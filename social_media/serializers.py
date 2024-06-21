from rest_framework import serializers
from .models import Post, Comment, InnerComment
from users.serializers import UserSerializer


class PostSerializerCreate(serializers.ModelSerializer):
    """
    Post Serializer.
    """

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "image",
            "video",
            "creat_time",
            "like_count",
            "you_liked",
            "comment_count",
            "user",
        ]
        extra_kwargs = {
            "like_count": {"read_only": True},
            "comment_count": {"read_only": True},
            "you_liked": {"read_only": True},
        }


class PostSerializer(serializers.ModelSerializer):
    """
    Post Serializer.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "image",
            "video",
            "creat_time",
            "like_count",
            "you_liked",
            "comment_count",
            "user",
        ]
        extra_kwargs = {
            "like_count": {"read_only": True},
            "comment_count": {"read_only": True},
            "you_liked": {"read_only": True},
        }


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer.
    """

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "like_count": {"read_only": True},
            "inner_comment_count": {"read_only": True},
        }


class InnerCommentSerializer(serializers.ModelSerializer):
    """
    InnerComment Serializer.
    """

    class Meta:
        model = InnerComment
        fields = "__all__"
        extra_kwargs = {"like_count": {"read_only": True}}
