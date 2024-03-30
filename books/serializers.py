from rest_framework import serializers
from .models import Book, BookSummary


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class BookSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSummary
        fields = "__all__"
