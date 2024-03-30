from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer, BookSummarySerializer
from .models import Book, BookSummary
from rest_framework import viewsets, pagination
from rest_framework import status


# Bais class of the pagination api classes
class BookPagination(pagination.PageNumberPagination):
    page_size = 4  # Number of books per page


class BookViewSet(viewsets.ModelViewSet):

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = BookPagination


class BookReview(viewsets.ModelViewSet):

    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def retrieve(self, request, pk):
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            serializer = self.serializer_class(queryset)
            if serializer.data["rating"] == None:
                return Response("there is no rate")
            else:
                return Response(serializer.data["rating"])
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookPaginationFilterGenre(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request, genre):
        try:
            queryset = self.get_queryset().filter(genre=genre)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Genre Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookPaginationFilterGenreAndPrice(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request, genre, min_value, max_value, order_from):
        try:
            if order_from == "DESC":
                queryset = (
                    self.get_queryset()
                    .filter(price__range=(min_value, max_value), genre=genre)
                    .order_by("-price")
                    .values()
                )
            else:
                queryset = (
                    self.get_queryset()
                    .filter(price__range=(min_value, max_value), genre=genre)
                    .order_by("price")
                    .values()
                )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Genre Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookPaginationFreeBooks(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request):
        try:
            queryset = self.get_queryset().filter(price=0)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Genre Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookPaginationHighRateBooks(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request):
        try:
            queryset = self.get_queryset().order_by("-rate").values()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Genre Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookPaginationPopularBooks(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request):
        try:
            queryset = (
                self.get_queryset()
                .order_by("-readers_count", "-to_read_count")
                .values()
            )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Genre Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookSearch(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, string):
        # Get search query parameter (e.g., ?query=anystr)
        # query = request.query_params.get("query")
        # if not query:
        #     return Response(
        #         {"error": "Missing search query like /book/search/?query=anystr"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        # Implement search logic based on the query string

        # Implement search logic based on the string
        queryset = (
            self.get_queryset().filter(title__icontains=string)
            | self.get_queryset().filter(author__icontains=string)
            | self.get_queryset().filter(genre__icontains=string)
            | self.get_queryset().filter(title__trigram_similar=string)
            | self.get_queryset().filter(author__trigram_similar=string)
            | self.get_queryset().filter(genre__trigram_similar=string)
            | self.get_queryset().filter(title__unaccent=string)
            | self.get_queryset().filter(author__unaccent=string)
            | self.get_queryset().filter(genre__unaccent=string)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class BookSummaryCreate(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSummarySerializer

    def create(self, request, book_id):
        try:
            book = self.get_queryset().get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookSummaryList(viewsets.ModelViewSet):
    queryset = BookSummary.objects.all()
    serializer_class = BookSummarySerializer

    def list(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset().filter(book=book)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class BookSummaryUpdate(viewsets.ModelViewSet):
    queryset = BookSummary.objects.all()
    serializer_class = BookSummarySerializer

    def update(self, request, book_id):
        try:
            bookSummary = self.get_queryset().get(id=book_id)
        except BookSummary.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(bookSummary, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookSummaryDelete(viewsets.ModelViewSet):
    queryset = BookSummary.objects.all()
    serializer_class = BookSummarySerializer

    def destroy(self, request, book_id):
        try:
            bookSummary = self.get_queryset().get(id=book_id)
        except BookSummary.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        bookSummary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
