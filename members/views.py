from django.http import JsonResponse
from .models import Member
from .serializers import MemberSerializer


def Member_list(request):
    if request.method == "GET":
        Members = Member.objects.all()
        serializer = MemberSerializer(Members, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        serializer = MemberSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def Member_detail(request, pk):
    try:
        Member = Member.objects.get(Member_id=pk)
    except Member.DoesNotExist:
        return JsonResponse({"error": "Member not found"}, status=404)

    if request.method == "GET":
        serializer = MemberSerializer(Member)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        serializer = MemberSerializer(Member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        Member.delete()
        return JsonResponse({"message": "Member deleted"}, status=204)
