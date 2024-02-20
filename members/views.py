from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Member
from .serializers import *


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
