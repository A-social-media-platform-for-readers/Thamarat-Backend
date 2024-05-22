from rest_framework import serializers
from .models import Post, Comment, InnerComment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "like_count": {"read_only": True},
            "comment_count": {"read_only": True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {"like_count": {"read_only": True}}


class InnerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerComment
        fields = "__all__"
        extra_kwargs = {"like_count": {"read_only": True}}
