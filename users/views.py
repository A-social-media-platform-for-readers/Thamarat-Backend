from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rest_framework import status
from rest_framework import viewsets


class RegisterView(viewsets.ModelViewSet):
    """
    Create a new user.
    """

    queryset = User.objects.none()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(viewsets.ModelViewSet):
    """
    User Login
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def login(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = self.get_queryset().filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
        return response


class UserView(viewsets.ModelViewSet):
    """
    Check Authentication and Retrieve User
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def check_auth(self, request):
        """
        Check Authentication function is used for view apis by
        import it in views.py to secure our apis
        """

        token = request.headers.get("Authorization")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        return payload

    def retrieve(self, request):
        """
        Retrieve User after checking authentication
        """

        payload = self.check_auth(request)
        user = self.get_queryset().filter(id=payload["id"]).first()
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class LogoutView(viewsets.ModelViewSet):
    """
    Logout User
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def logout(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response
