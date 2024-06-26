from rest_framework.response import Response
from .serializers import (
    PostSerializerCreate,
    PostSerializer,
    CommentSerializerCreate,
    CommentSerializer,
    InnerCommentSerializerCreate,
    InnerCommentSerializer,
    MessageSerializerCreate,
    MessageSerializer,
)
from .models import Post, Comment, InnerComment, Message
from users.models import User
from rest_framework import viewsets, pagination
from rest_framework import status
from users.views import UserView


class PaginationNumber(pagination.PageNumberPagination):
    """
    PaginatPostion class for Post objects.

    This class defines the page size for paginated responses.

    Attributes:
        page_size (int): The number of posts to display per page.
            Default is 5.
    """

    page_size = 5


class PostCreate(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializerCreate
    pagination_class = PaginationNumber

    def create(self, request):
        """
        Create a new post.
        """
        request.data["user"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostUserList(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PaginationNumber

    def list(self, request, user_id):
        """
        List posts by pagination pages(5 by 5).
        """

        user = User.objects.filter(id=user_id).first()
        queryset = self.get_queryset().filter(user=user)
        for post in queryset:
            if user in post.liked_users.all():
                post.you_liked = True
                post.save()
            else:
                post.you_liked = False
                post.save()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PaginationNumber

    def list(self, request):
        """
        List posts by pagination pages(5 by 5).
        """
        user = request.user
        queryset = self.get_queryset()
        for post in queryset:
            if user in post.liked_users.all():
                post.you_liked = True
                post.save()
            else:
                post.you_liked = False
                post.save()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, post_id):
        """
        Retrieve a post.
        """

        user = request.user
        try:
            queryset = self.get_queryset().filter(id=post_id).first()
            if user in queryset.liked_users.all():
                queryset.you_liked = True
                queryset.save()
            else:
                queryset.you_liked = False
                queryset.save()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response("Post Not Found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, post_id):
        """
        Update a post.
        """
        post = self.get_queryset().filter(id=post_id).first()
        if post is not None:
            if request.user.id != post.user.id:
                return Response(
                    "You are not authorized to update this post",
                    status=status.HTTP_403_FORBIDDEN,
                )
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, post_id):
        """
        Delete a post.
        """
        try:
            post = self.get_queryset().filter(id=post_id).first()
            if post is not None:
                if request.user.id != post.user.id:
                    return Response(
                        "You are not authorized to delete this post",
                        status=status.HTTP_403_FORBIDDEN,
                    )
            post.delete()
            return Response("Post Deleted")
        except:
            return Response("Post Not Found", status=status.HTTP_400_BAD_REQUEST)


class PostLikeViewSet(viewsets.ModelViewSet):
    """
    Post like counter.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def like(self, request, post_id):
        """
        Like a Post(add one to likes count).

        Note: request body is not required.
        """
        user = request.user
        post = self.get_queryset().filter(id=post_id).first()
        post.liked_users.add(user)
        post.like()
        return Response("Post Liked", status=status.HTTP_201_CREATED)

    def unlike(self, request, post_id):
        """
        Unlike a Post(subtract one form likes count).
        """
        user = request.user
        post = self.get_queryset().filter(id=post_id).first()
        post.liked_users.remove(user)
        post.remove_like()
        return Response("Post Unliked", status=status.HTTP_201_CREATED)


class CommentCreate(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializerCreate
    pagination_class = PaginationNumber

    def create(self, request):
        """
        Create a new comment.
        """
        request.data["user"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        post = Post.objects.filter(id=request.data["post"]).first()
        post.add_comment()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment viewset.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PaginationNumber

    def list(self, request, post_id):
        """
        List comments by pagination pages(5 by 5).
        """
        user = request.user
        post = Post.objects.filter(id=post_id).first()
        queryset = self.get_queryset().filter(post=post)
        for comment in queryset:
            if user in comment.liked_users.all():
                comment.you_liked = True
                comment.save()
            else:
                comment.you_liked = False
                comment.save()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, comment_id):
        """
        Retrieve a comment.
        """
        user = request.user
        try:
            queryset = self.get_queryset().filter(id=comment_id).first()
            if user in queryset.liked_users.all():
                queryset.you_liked = True
                queryset.save()
            else:
                queryset.you_liked = False
                queryset.save()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response("Comment Not Found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, comment_id):
        """
        Update a comment.
        """
        comment = self.get_queryset().filter(id=comment_id).first()
        if comment is not None:
            if request.user.id != comment.user.id:
                return Response(
                    "You are not authorized to update this comment",
                    status=status.HTTP_403_FORBIDDEN,
                )
        serializer = self.serializer_class(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, comment_id):
        """
        Delete a comment.
        """
        try:
            comment = self.get_queryset().filter(id=comment_id).first()
            if comment is not None:
                if request.user.id != comment.user.id:
                    return Response(
                        "You are not authorized to delete this comment",
                        status=status.HTTP_403_FORBIDDEN,
                    )
            comment.post.remove_comment()
            comment.delete()
            return Response("Comment Deleted")
        except:
            return Response("Comment Not Found", status=status.HTTP_400_BAD_REQUEST)


class CommentLikeViewSet(viewsets.ModelViewSet):
    """
    Comment like counter
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def like(self, request, comment_id):
        """
        Like a Comment(add one to likes count).

        Note: request body is not required.
        """
        user = request.user
        comment = self.get_queryset().filter(id=comment_id).first()
        comment.liked_users.add(user)
        comment.like()
        return Response("Comment Liked", status=status.HTTP_201_CREATED)

    def unlike(self, request, comment_id):
        """
        Unlike a Comment(subtract one form likes count).
        """
        user = request.user
        comment = self.get_queryset().filter(id=comment_id).first()
        comment.liked_users.remove(user)
        comment.remove_like()
        return Response("Comment Unliked", status=status.HTTP_201_CREATED)


class InnerCommentCreate(viewsets.ModelViewSet):
    """
    API endpoint that allows InnerComments to be viewed or edited.
    """

    queryset = InnerComment.objects.all()
    serializer_class = InnerCommentSerializerCreate
    pagination_class = PaginationNumber

    def create(self, request):
        """
        Create a new InnerComment.
        """
        request.data["user"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        comment = Comment.objects.filter(id=request.data["comment"]).first()
        comment.add_inner_comment()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InnerCommentViewSet(viewsets.ModelViewSet):
    """
    InnerComment viewset.
    """

    queryset = InnerComment.objects.all()
    serializer_class = InnerCommentSerializer
    pagination_class = PaginationNumber

    def list(self, request, comment_id):
        """
        List InnerComments by pagination pages(5 by 5).
        """
        user = request.user
        comment = Comment.objects.filter(id=comment_id).first()
        queryset = self.get_queryset().filter(comment=comment)
        for inner_comment in queryset:
            if user in inner_comment.liked_users.all():
                inner_comment.you_liked = True
                inner_comment.save()
            else:
                inner_comment.you_liked = False
                inner_comment.save()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, inner_comment_id):
        """
        Retrieve a InnerComment.
        """
        user = request.user
        try:
            queryset = self.get_queryset().filter(id=inner_comment_id).first()
            if user in queryset.liked_users.all():
                queryset.you_liked = True
                queryset.save()
            else:
                queryset.you_liked = False
                queryset.save()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response(
                "InnerComment Not Found", status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, inner_comment_id):
        """
        Update a InnerComment.
        """
        inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
        if inner_comment is not None:
            if request.user.id != inner_comment.user.id:
                return Response(
                    "You are not authorized to update this InnerComment",
                    status=status.HTTP_403_FORBIDDEN,
                )
        serializer = self.serializer_class(inner_comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, inner_comment_id):
        """
        Delete a InnerComment.
        """
        try:
            inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
            if inner_comment is not None:
                if request.user.id != inner_comment.user.id:
                    return Response(
                        "You are not authorized to delete this InnerComment",
                        status=status.HTTP_403_FORBIDDEN,
                    )
            inner_comment.comment.remove_inner_comment()
            inner_comment.delete()
            return Response("InnerComment Deleted")
        except:
            return Response(
                "InnerComment Not Found", status=status.HTTP_400_BAD_REQUEST
            )


class InnerCommentLikeViewSet(viewsets.ModelViewSet):
    """
    InnerComment like counter.
    """

    queryset = InnerComment.objects.all()
    serializer_class = InnerCommentSerializer

    def like(self, request, inner_comment_id):
        """
        Like a InnerComment(add one to likes count).

        Note: request body is not required.
        """
        user = request.user
        inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
        inner_comment.liked_users.add(user)
        inner_comment.like()
        return Response("InnerComment Liked", status=status.HTTP_201_CREATED)

    def unlike(self, request, inner_comment_id):
        """
        Unlike a InnerComment(subtract one form likes count).
        """
        user = request.user
        inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
        inner_comment.liked_users.remove(user)
        inner_comment.remove_like()
        return Response("InnerComment Unliked", status=status.HTTP_201_CREATED)


class MessageCreate(viewsets.ModelViewSet):
    """
    Create Message.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializerCreate

    def create(self, request):
        """
        Create a new Message.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Message Viewset.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def list(self, request):
        """
        List Messages.
        """

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, message_id):
        """
        Retrieve a Message.
        """

        try:
            message = self.get_queryset().filter(id=message_id).first()
            serializer = self.serializer_class(message)
            return Response(serializer.data)
        except:
            return Response("Message Not Found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, message_id):
        """
        Update a Message.
        """
        try:
            message = self.get_queryset().filter(id=message_id).first()
            if message is not None:
                if request.user.id != message.sender.id:
                    return Response(
                        "You are not authorized to update this Message",
                        status=status.HTTP_403_FORBIDDEN,
                    )
            serializer = self.serializer_class(message, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response("Message Not Found", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, message_id):
        """
        Delete a Message.
        """
        try:
            message = self.get_queryset().filter(id=message_id).first()
            if message is not None:
                if request.user.id != message.sender.id:
                    return Response(
                        "You are not authorized to delete this Message",
                        status=status.HTTP_403_FORBIDDEN,
                    )
            message.delete()
            return Response("Message Deleted")
        except:
            return Response("Message Not Found", status=status.HTTP_400_BAD_REQUEST)
