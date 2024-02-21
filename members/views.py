from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Member
from .serializers import *
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework import authentication, permissions
from django.contrib.auth.models import User


# @api_view(["GET", "POST"])
# def Member_list(request):
#     if request.method == "GET":
#         Members = Member.objects.all()
#         serializer = MemberSerializer(Members, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         # data = JSONParser().parse(request)
#         serializer = MemberSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "PUT", "DELETE"])
# def Member_detail(request, pk):
#     try:
#         member = Member.objects.get(pk=pk)
#     except Member.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = MemberSerializer(Member)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = MemberSerializer(Member, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == "DELETE":
#         Member.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only Authenticated users are able to access this view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


@api_view(["GET", "POST"])
def read_All_Create_Members(req):
    if req.method == "GET":
        Members = Member.objects.all()
        jsndata = MemberSerializer(Members, many=True).data
        return Response({"data": jsndata}, status=status.HTTP_200_OK)

    elif req.method == "POST":
        member = MemberSerializer(data=req.data)
        if member.is_valid():
            member.save()
            return Response(member.data, status=status.HTTP_201_CREATED)
        return Response(member.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE", "PATCH", "PUT"])
def apis_Member(req, ID):
    if req.method == "GET":
        obj = Member.objects.get(id=ID)
        jsndata = MemberSerializer(obj, many=False).data
        finaldata = {"data": jsndata}
        return Response(data=finaldata, status=status.HTTP_200_OK)

    if req.method == "DELETE":
        Member.objects.filter(id=ID).delete()
        return Response(status.HTTP_204_NO_CONTENT)

    if req.method == "PATCH":
        t = Member.objects.get(id=ID)
        st = MemberSerializer(instance=t, data=req.data, partial=True)
        if st.is_valid():
            st.save()
            return Response(status.HTTP_200_OK)
        return Response(st.errors, status=status.HTTP_400_BAD_REQUEST)

    if req.method == "PUT":
        t = Member.objects.get(id=ID)
        st = MemberSerializer(instance=t, data=req.data, partial=False)
        if st.is_valid():
            st.save()
            return Response(status.HTTP_200_OK)
        return Response(st.errors, status=status.HTTP_400_BAD_REQUEST)
