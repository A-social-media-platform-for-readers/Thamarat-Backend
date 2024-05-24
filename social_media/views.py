from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, InnerCommentSerializer
from .models import Post, Comment, InnerComment
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


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PaginationNumber

    def list(self, request):
        """
        Retrieve all posts.
        """
        UserView.check_auth(self, request)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new post.
        """
        UserView.check_auth(self, request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        """
        Retrieve a post.
        """
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response("Post Not Found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """
        Update a post.
        """
        payload = UserView.check_auth(self, request)
        user_id = payload["id"]
        post = self.get_queryset().filter(id=pk).first()
        if post is not None:
            if user_id != post.user.id:
                return Response(
                    "You are not authorized to update this post",
                    status=status.HTTP_403_FORBIDDEN,
                )
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """
        Delete a post.
        """
        payload = UserView.check_auth(self, request)
        user_id = payload["id"]
        try:
            post = self.get_queryset().filter(id=pk).first()
            if post is not None:
                if user_id != post.user.id:
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
    Post like counter
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def like(self, request, pk):
        """
        Like a post.
        """
        UserView.check_auth(self, request)
        post = self.get_queryset().filter(id=pk).first()
        post.like()
        return Response("Post Liked", status=status.HTTP_201_CREATED)

    def unlike(self, request, pk):
        """
        Unlike a post.
        """
        UserView.check_auth(self, request)
        post = self.get_queryset().filter(id=pk).first()
        post.remove_like()
        return Response("Post Unliked", status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Comment viewset
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PaginationNumber

    def list(self, request, post_id):
        """
        Retrieve all comments.
        """
        UserView.check_auth(self, request)
        post = Post.objects.filter(id=post_id).first()
        queryset = self.get_queryset().filter(post=post)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, post_id):
        """
        Create a new comment.
        """
        UserView.check_auth(self, request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        post = Post.objects.filter(id=post_id).first()
        post.add_comment()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, comment_id):
        """
        Retrieve a comment.
        """
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=comment_id).first()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response("Comment Not Found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, comment_id):
        """
        Update a comment.
        """
        payload = UserView.check_auth(self, request)
        user_id = payload["id"]
        comment = self.get_queryset().filter(id=comment_id).first()
        if comment is not None:
            if user_id != comment.user.id:
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
        payload = UserView.check_auth(self, request)
        user_id = payload["id"]
        try:
            comment = self.get_queryset().filter(id=comment_id).first()
            if comment is not None:
                if user_id != comment.user.id:
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
        Like a comment.
        """
        UserView.check_auth(self, request)
        comment = self.get_queryset().filter(id=comment_id).first()
        comment.like()
        return Response("Comment Liked", status=status.HTTP_201_CREATED)

    def unlike(self, request, comment_id):
        """
        Unlike a comment.
        """
        UserView.check_auth(self, request)
        comment = self.get_queryset().filter(id=comment_id).first()
        comment.remove_like()
        return Response("Comment Unliked", status=status.HTTP_201_CREATED)


class InnerCommentViewSet(viewsets.ModelViewSet):
    """
    InnerComment viewset
    """

    queryset = InnerComment.objects.all()
    serializer_class = InnerCommentSerializer
    pagination_class = PaginationNumber

    def list(self, request, comment_id):
        """
        Retrieve all InnerComments.
        """
        UserView.check_auth(self, request)
        comment = Comment.objects.filter(id=comment_id).first()
        queryset = self.get_queryset().filter(comment=comment)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, comment_id):
        """
        Create a new InnerComment.
        """
        UserView.check_auth(self, request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        comment = Comment.objects.filter(id=comment_id).first()
        comment.add_inner_comment()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, inner_comment_id):
        """
        Retrieve a InnerComment.
        """
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=inner_comment_id).first()
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
        payload = UserView.check_auth(self, request)
        user_id = payload["id"]
        inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
        if inner_comment is not None:
            if user_id != inner_comment.user.id:
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
        payload = UserView.check_auth(self, request)
        user_id = payload["id"]
        try:
            inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
            if inner_comment is not None:
                if user_id != inner_comment.user.id:
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
    InnerComment like counter
    """

    queryset = InnerComment.objects.all()
    serializer_class = InnerCommentSerializer

    def like(self, request, inner_comment_id):
        """
        Like a InnerComment.
        """
        UserView.check_auth(self, request)
        inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
        inner_comment.like()
        return Response("InnerComment Liked", status=status.HTTP_201_CREATED)

    def unlike(self, request, inner_comment_id):
        """
        Unlike a InnerComment.
        """
        UserView.check_auth(self, request)
        inner_comment = self.get_queryset().filter(id=inner_comment_id).first()
        inner_comment.remove_like()
        return Response("InnerComment Unliked", status=status.HTTP_201_CREATED)
