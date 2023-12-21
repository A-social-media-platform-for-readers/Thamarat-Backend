from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Member
from .serializers import MemberSerializer


@csrf_exempt
def Member_list(request):
    if request.method == "GET":
        Members = Member.objects.all()
        serializer = MemberSerializer(Members, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == "POST":
        # data = JSONParser().parse(request)
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def Member_detail(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = MemberSerializer(Member)
        return JsonResponse(serializer.data)
    
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = MemberSerializer(Member, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == "DELETE":
        Member.delete()
        return HttpResponse(status=204)
