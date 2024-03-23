from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer
from .models import Book
from rest_framework import viewsets, pagination
from rest_framework import status


class CreateBook(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListAllBooks(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


# start of the pagination api
class BookPagination(pagination.PageNumberPagination):
    page_size = 4  # Number of books per page (default)


# api to get some(4) books for every request
# like facebook timeline
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)


# api to get some(4) books after filer them
# for every request
# like facebook timeline
class BookFilter(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request, genre):
        queryset = self.get_queryset().filter(genre="sasa")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


# end of the pagination api


class RetrieveBook(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class UpdateBook(APIView):
    def put(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(instance=book, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class DeleteBook(APIView):
    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response("Book Deleted")
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class ReviewBook(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book)
            if serializer.data["rating"] == None:
                return Response("there is no rate")
            else:
                return Response(serializer.data["rating"])
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookSearchView(APIView):
    def get(self, request):
        # Get search query parameter (e.g., ?query=anystr)
        query = request.query_params.get("query")
        if not query:
            return Response(
                {"error": "Missing search query like ?query=anystr"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Implement search logic based on the query string
        books = (
            Book.objects.filter(title__icontains=query)
            | Book.objects.filter(author__icontains=query)
            | Book.objects.filter(genre__icontains=query)
            | Book.objects.filter(title__trigram_similar=query)
            | Book.objects.filter(author__trigram_similar=query)
            | Book.objects.filter(genre__trigram_similar=query)
            | Book.objects.filter(title__unaccent=query)
            | Book.objects.filter(author__unaccent=query)
            | Book.objects.filter(genre__unaccent=query)
        )
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
