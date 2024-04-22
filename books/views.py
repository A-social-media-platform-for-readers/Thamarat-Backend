from rest_framework.response import Response
from .serializers import BookSerializer, BookSummarySerializer
from .models import Book, BookSummary
from rest_framework import viewsets, pagination
from rest_framework import status
from users.views import UserView


class BookPagination(pagination.PageNumberPagination):
    """
    Pagination class for Book objects.

    This class defines the page size for paginated responses.

    Attributes:
        page_size (int): The number of books to display per page.
            Default is 4.
    """

    page_size = 4


class BookViewSet(viewsets.ModelViewSet):
    """
    Class that allows CRUD operations for Book objects.

    Retreives the books by pagination pages.
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = BookPagination

    def list(self, request):
        UserView.check_auth(self, request)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        UserView.check_auth(self, request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            serializer = self.serializer_class(queryset, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            serializer = self.serializer_class(
                queryset, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            queryset.delete()
            return Response("Book Deleted")
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookReview(viewsets.ModelViewSet):
    """
    Api to retreive the review of a book
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def retrieve(self, request, pk):
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(id=pk).first()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data["rate"])
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookFilterGenre(viewsets.ModelViewSet):
    """
    Filter books by genre.

    Retreive the books by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request, genre):
        UserView.check_auth(self, request)
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


class BookFilterGenreAndPrice(viewsets.ModelViewSet):
    """
    Filter books by genre and price range.

    Retreive the books by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request, genre, min_value, max_value, order_from):
        """
        Filter books by genre and price range,
        with the option to order by price in ascending or descending order.

        Args:
            request (rest_framework.request.Request): The request object.
            genre (str): The genre of the books.
            min_value (int): The minimum price of the books.
            max_value (int): The maximum price of the books.
            order_from (str): The order in which to sort the books "DESC" for
                descending order, any string else for ascending order.

        Retreive the books by pagination pages.
        """
        UserView.check_auth(self, request)
        try:
            if order_from == "DESC":
                queryset = (
                    self.get_queryset()
                    .filter(price__range=(min_value, max_value), genre=genre)
                    .order_by("-price")
                )
            else:
                queryset = (
                    self.get_queryset()
                    .filter(price__range=(min_value, max_value), genre=genre)
                    .order_by("price")
                )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(
                "Genre Not Found Or Price Range Not Found",
                status=status.HTTP_400_BAD_REQUEST,
            )


class FreeBooks(viewsets.ModelViewSet):
    """
    Retreive the free books by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request):
        UserView.check_auth(self, request)
        try:
            queryset = self.get_queryset().filter(price=0)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(
                "There is no free books", status=status.HTTP_400_BAD_REQUEST
            )


class HigherRatingBooks(viewsets.ModelViewSet):
    """
    Retreive books with higher rating by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request):
        UserView.check_auth(self, request)
        queryset = self.get_queryset().order_by("-rate")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PopularBooks(viewsets.ModelViewSet):
    """
    Retreive the popular books by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request):
        UserView.check_auth(self, request)
        queryset = self.get_queryset().order_by("-readers_count", "-to_read_count")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookSearch(viewsets.ModelViewSet):
    """
    Search books by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

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
        UserView.check_auth(self, request)
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
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


######################### book summary views ##########################


class BookSummaryCreate(viewsets.ModelViewSet):
    """
    Create book summary.
    """

    queryset = Book.objects.all()
    serializer_class = BookSummarySerializer

    def create(self, request, book_id):
        UserView.check_auth(self, request)
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
    """
    List book summaries.
    """

    queryset = BookSummary.objects.all()
    serializer_class = BookSummarySerializer

    def list(self, request, book_id):
        UserView.check_auth(self, request)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset().filter(book=book)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class BookSummaryUdateDelete(viewsets.ModelViewSet):
    """
    Book summary views for update and delete.
    """

    queryset = BookSummary.objects.all()
    serializer_class = BookSummarySerializer

    def update(self, request, book_id, summary_id):
        UserView.check_auth(self, request)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            bookSummary = self.get_queryset().filter(book=book, id=summary_id)
        except BookSummary.DoesNotExist:
            return Response(
                {"error": "Book summary not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(bookSummary, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, book_id, summary_id):
        UserView.check_auth(self, request)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            bookSummary = self.get_queryset().filter(book=book, id=summary_id)
        except BookSummary.DoesNotExist:
            return Response(
                {"error": "Book summary not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        bookSummary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
