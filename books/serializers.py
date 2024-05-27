from rest_framework import serializers
from .models import Book, BookSummary, BookReview, BookReaders, BookToRead, BookReading
from users.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model
    """

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "rate",
            "price",
            "genre",
            "publisher",
            "publication_date",
            "description",
            "reviwes_count",
            "readers_count",
            "reading_count",
            "to_read_count",
            "cover_image",
            "pdf_file",
        ]
        extra_kwargs = {
            "rate": {"read_only": True},
            "reviwes_count": {"read_only": True},
            "readers_count": {"read_only": True},
            "reading_count": {"read_only": True},
            "to_read_count": {"read_only": True},
        }


class BookSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for Book summary model
    """

    class Meta:
        model = BookSummary
        fields = "__all__"


class BookReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for BookReview model
    """

    class Meta:
        model = BookReview
        fields = "__all__"
        extra_kwargs = {
            "created_time": {"read_only": True},
            "like_count": {"read_only": True},
        }


class BookReadersSerializer(serializers.ModelSerializer):
    """
    Serializer for BookReaders model
    """

    class Meta:
        model = BookReaders
        fields = "__all__"


class BookReadingSerializer(serializers.ModelSerializer):
    """
    Serializer for BookReading model
    """

    class Meta:
        model = BookReading
        fields = "__all__"


class BookToReadSerializer(serializers.ModelSerializer):
    """
    Serializer for BookToRead model
    """

    class Meta:
        model = BookToRead
        fields = "__all__"
