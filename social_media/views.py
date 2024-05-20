from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post
from rest_framework import viewsets, pagination
from rest_framework import status
from users.views import UserView


class PostPagination(pagination.PageNumberPagination):
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
    pagination_class = PostPagination

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

        UserView.check_auth(self, request)
        post = self.get_queryset().filter(id=pk).first()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """
        Delete a post.
        """

        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            queryset.delete()
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
