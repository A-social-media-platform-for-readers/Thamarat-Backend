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


@api_view(['GET'])
def all_Member(req):
    
    objs = Member.objects.all()
    jsndata = MemberSerializer(objs, many=True).data
    finaldata = {'data': jsndata}

    return Response(data=finaldata, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_Member(req):
    
    Member = MemberSerializer(data=req.data)
    if (Member.is_valid()):

        Member.save()

    return Response(status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_Member(req, ID):
    
    Member.objects.filter(id=ID).delete()

    return Response(status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_Member(req, ID):
    
    t = Member.objects.filter(id=ID)[0]
    st = MemberSerializer(instance=t, data=req.data, partial=True)
    
    if (st.is_valid()):
        
        st.save()

    return Response(status.HTTP_200_OK)
