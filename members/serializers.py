from rest_framework import serializers
from .models import Gender, Address, Member, Reader, Author, PublishingHouse


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class ReaderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reader
		fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Author
		fields = "__all__"


class PublishingHouseSerializer(serializers.ModelSerializer):
	class Meta:
		model = PublishingHouse
		fields = "__all__"
