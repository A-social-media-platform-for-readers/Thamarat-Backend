from rest_framework import serializers
from .models import Book, BookSummary


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model
    """

    class Meta:
        model = Book
        fields = "__all__"


class BookSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for Book summary model
    """

    class Meta:
        model = BookSummary
        fields = "__all__"
