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
        """
        User Login
        """
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
        token = request.headers.get("Authorization") or request.COOKIES.get("jwt")

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


class UserViewSet(viewsets.ModelViewSet):
    """
    User CRUD
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        """
        List Users
        """
        UserView.check_auth(self, request)
        user = self.get_queryset()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """
        Retrieve user by id
        """
        UserView.check_auth(self, request)
        user = self.get_queryset().filter(id=pk).first()
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Update User
        """
        UserView.check_auth(self, request)
        user = self.get_queryset().filter(id=pk).first()
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """
        Delete User
        """
        UserView.check_auth(self, request)
        user = self.get_queryset().filter(id=pk).first()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutView(viewsets.ModelViewSet):
    """
    Logout User
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def logout(self, request):
        """
        User Logout
        """
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response


class FollowView(viewsets.ModelViewSet):
    """
    Follow User
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def follow(self, request, user_to_follow_id, user_to_followed_id):
        """
        Follow User
        """
        UserView.check_auth(self, request)
        user_to_follow = self.get_queryset().filter(id=user_to_follow_id).first()
        user_to_followed = self.get_queryset().filter(id=user_to_followed_id).first()
        user_to_follow.following.add(user_to_followed)
        user_to_follow.save()
        user_to_followed.followers.add(user_to_follow)
        user_to_followed.save()
        return Response({"message": "success"})

    def unfollow(self, request, user_to_unfollow_id, user_to_unfollowed_id):
        """
        Unfollow User
        """
        UserView.check_auth(self, request)
        user_to_unfollow = self.get_queryset().filter(id=user_to_unfollow_id).first()
        user_to_unfollowed = (
            self.get_queryset().filter(id=user_to_unfollowed_id).first()
        )
        user_to_unfollow.following.remove(user_to_unfollowed)
        user_to_unfollow.save()
        user_to_unfollowed.followers.remove(user_to_unfollow)
        user_to_unfollowed.save()
        return Response({"message": "success"})

    def followers(self, request, user_id):
        """
        Get Followers
        """
        UserView.check_auth(self, request)
        user = self.get_queryset().filter(id=user_id).first()
        follower = user.followers
        serializer = self.serializer_class(follower, many=True)
        return Response(serializer.data)

    def following(self, request, user_id):
        """
        Get Following
        """
        UserView.check_auth(self, request)
        user = self.get_queryset().filter(id=user_id).first()
        follower = user.following
        serializer = self.serializer_class(follower, many=True)
        return Response(serializer.data)
