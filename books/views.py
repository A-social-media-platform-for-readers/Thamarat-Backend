from rest_framework import viewsets, pagination
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.http import FileResponse, HttpResponseNotFound
from users.models import User
from users.views import UserView
from .serializers import (
    BookSerializer,
    BookUserSerializer,
    BookSummarySerializer,
    BookReadersSerializer,
    BookToReadSerializer,
    BookReadingSerializer,
    BookReviewSerializer,
)
from .models import (
    Book,
    BookSummary,
    BookReaders,
    BookReading,
    BookToRead,
    BookReview,
)


class BookPagination6(pagination.PageNumberPagination):
    """
    Pagination class for Book objects.

    This class defines the page size for paginated responses.

    Attributes:
        page_size (int): The number of books to display per page.
            Default is 6.
    """

    page_size = 6


class BookViewSet6(viewsets.ModelViewSet):
    """
    Book view set for paginated responses 6 books by request
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = BookPagination6

    def list(self, request):
        """
        List 6 books per request.
        """

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
        """
        List 4 books per request.
        """

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """
        retrieve one book by id.
        """

        try:
            queryset = self.get_queryset().filter(id=pk).first()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        Create new book.
        """
        user = request.user
        book = self.serializer_class(data=request.data)
        book.is_valid(raise_exception=True)
        book.save()
        user.our_books.add(book.data["id"])
        user.save()
        return Response(book.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """
        Update book by id.
        """

        queryset = self.get_queryset().filter(id=pk).first()
        serializer = self.serializer_class(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        """
        Partial update book by id.
        """

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
        """
        Delete book by id.
        """

        try:
            queryset = self.get_queryset().filter(id=pk).first()
            queryset.delete()
            return Response("Book Deleted")
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookUserList(viewsets.ModelViewSet):
    """
    List all user 's books.
    """

    serializer_class = BookUserSerializer
    queryset = User.objects.all()

    def list(self, request, user_id):
        """
        List all user 's books.
        """

        queryset = self.get_queryset().filter(id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookDownload(viewsets.ModelViewSet):
    """Download book pdf"""

    def download_book_pdf(self, request, book_id):
        """Download book pdf"""

        book = get_object_or_404(Book, id=book_id)
        if book.pdf_file:
            response = FileResponse(
                book.pdf_file.open("rb"),
                as_attachment=True,
                filename=book.pdf_file.name,
            )
            return response
        else:
            return HttpResponseNotFound("The requested book does not have a PDF file.")


class BookCoverDownload(viewsets.ModelViewSet):
    """Download book cover"""

    def download_book_cover(self, request, book_id):
        """Download book cover"""

        book = get_object_or_404(Book, id=book_id)
        if book.cover_image:
            response = FileResponse(
                book.cover_image.open("rb"),
                as_attachment=True,
                filename=book.cover_image.name,
            )
            return response
        else:
            return HttpResponseNotFound(
                "The requested book does not have a cover image."
            )


class BookRate(viewsets.ModelViewSet):
    """
    Book rate view.
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def rate(self, request, book_id, rating):
        """
        Book rate.

        Parameters:
            book_id (int): book id to rate it.
            rating (float): accept float or integer numbers.
        """
        user = request.user
        try:
            book = self.get_queryset().filter(id=book_id).first()
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)
        if user in book.rate_users.all():
            return Response(
                "You Already Rated This Book", status=status.HTTP_400_BAD_REQUEST
            )
        book.calc_rate(rating)
        book.rate_users.add(user)
        book.save()
        return Response("Book Rated", status=status.HTTP_201_CREATED)


class WantToRead(viewsets.ModelViewSet):
    """
    Book want to read view.
    """

    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def readed(self, request, book_id):
        """
        Add book to readed books.

        Note: request body is not required.
        """
        try:
            book = self.get_queryset().filter(id=book_id).first()
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)
        serializer = BookReadersSerializer(
            data={"reader": [request.user.id], "book": [book.id]}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book.add_reader()
        return Response("Book Added To Readed Books")

    def reading(self, request, book_id):
        """
        Add book to reading books.

        Note: request body is not required.
        """
        try:
            book = self.get_queryset().filter(id=book_id).first()
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)
        serializer = BookReadingSerializer(
            data={"reader": [request.user.id], "book": [book.id]}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book.add_reading()
        return Response("Book Added To Reading Books")

    def want_to_read(self, request, book_id):
        """
        Add book to want to read books.

        Note: request body is not required.
        """
        try:
            book = self.get_queryset().filter(id=book_id).first()
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)
        serializer = BookToReadSerializer(
            data={"reader": [request.user.id], "book": [book.id]}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book.add_to_read()
        return Response("Book Added To Want To Read")

    def get_readed_books(self, request):
        """
        List my readed books.
        """
        user = request.user
        books_reader = BookReaders.objects.filter(reader=user)
        books = []
        for i in range(len(books_reader)):
            book = BookSerializer(books_reader[i].book, many=True)
            books.append(book.data[0])
        return Response(books)

    def get_reading_books(self, request):
        """
        List my reading books.
        """
        user = request.user
        books_reading = BookReading.objects.filter(reader=user)
        books = []
        for i in range(len(books_reading)):
            book = BookSerializer(books_reading[i].book, many=True)
            books.append(book.data[0])
        return Response(books)

    def get_to_read_books(self, request):
        """
        List my want to read books.
        """
        user = request.user
        books_to_read = BookToRead.objects.filter(reader=user)
        books = []
        for i in range(len(books_to_read)):
            book = BookSerializer(books_to_read[i].book, many=True)
            books.append(book.data[0])
        return Response(books)

    def delete_readed_book(self, request, book_id):
        """
        Delete book from readed books.
        """
        try:
            book = self.get_queryset().filter(id=book_id).first()
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)
        book_reader = BookReaders.objects.filter(reader=request.user.id, book=book_id)
        book_reader.delete()
        book.remove_reader()
        return Response("Book Removed From Readed Books")

    def delete_reading_book(self, request, book_id):
        """
        Delete book from reading books.
        """
        try:
            book = self.get_queryset().filter(id=book_id).first()
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)
        book_reading = BookReading.objects.filter(reader=request.user.id, book=book_id)
        book_reading.delete()
        book.remove_reading()
        return Response("Book Removed From reading Books")

    def delete_to_read_book(self, request, book_id):
        """
        Delete book from want to read books.
        """
        try:
            book = self.get_queryset().filter(id=book_id).first()
        except:
            return Response("Book Not Found", status=status.HTTP_400_BAD_REQUEST)
        book_to_read = BookToRead.objects.filter(reader=request.user.id, book=book_id)
        book_to_read.delete()
        book.remove_to_read()
        return Response("Book Removed From To Read Books")


class BookReviewView(viewsets.ModelViewSet):
    """
    BookReview Apis
    """

    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()

    def list(self, request, book_id):
        """
        List book reviews.
        """

        book = Book.objects.get(id=book_id)
        queryset = self.get_queryset().filter(book=book)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, book_id):
        """
        Create new book review.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        book = Book.objects.get(id=book_id)
        book.add_reviwe()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, Review_id):
        """
        Retreive book review by id.
        """

        try:
            queryset = self.get_queryset().filter(id=Review_id).first()
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response("Review Not Found", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, Review_id):
        """
        Udate book review.
        """

        queryset = self.get_queryset().filter(id=Review_id).first()
        serializer = self.serializer_class(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, Review_id, book_id):
        """
        Delete book review.
        """

        try:
            queryset = self.get_queryset().filter(id=Review_id).first()
            book = Book.objects.get(id=book_id)
            book.remove_reviwe()
            queryset.delete()
            return Response("Review Deleted")
        except:
            return Response("Review Not Found", status=status.HTTP_400_BAD_REQUEST)


class BookReviewLikes(viewsets.ModelViewSet):
    """
    Review like and unlike
    """

    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()

    def like(self, request, Review_id):
        """
        Like a Review(add one to likes count).

        Note: request body is not required.
        """

        review = self.get_queryset().filter(id=Review_id).first()
        review.like()
        return Response("Review Liked", status=status.HTTP_201_CREATED)

    def unlike(self, request, Review_id):
        """
        Unlike a Review(subtract one form likes count).
        """

        review = self.get_queryset().filter(id=Review_id).first()
        review.remove_like()
        return Response("Review Unliked", status=status.HTTP_201_CREATED)


class BookFilterGenre(viewsets.ModelViewSet):
    """
    Filter books by genre.

    Retreive the books by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request, genre):
        """
        Filter books by genre.

        Return:
            the books by pagination pages(4 by 4).
        """

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

        Parameters:
            genre (str): The genre of the books.
            min_value (int): The minimum price of the books.
            max_value (int): The maximum price of the books.
            order_from (str): The order in which to sort the books, "DESC" for
                descending order, any string else for ascending order.

        Return:
            the books by pagination pages(4 by 4)
        """

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
        """
        Retreive the free books by pagination pages(4 by 4).
        """

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
        """
        Retreive books with higher rating by pagination pages(4 by 4).
        """

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
        """
        Retreive the popular books depend on readers_count,
        reading_count and to_read_count by pagination pages(4 by 4).
        """

        queryset = self.get_queryset().order_by(
            "-readers_count", "-reading_count", "-to_read_count"
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookSearch(viewsets.ModelViewSet):
    """
    Search books and list them by pagination pages.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def list(self, request, string):
        """
        Search books and list them by pagination pages(4 by 4).

        Note: the input string search can be near from the actual string.
        """
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
        """
        Create book summary.

        Note: should upload a book summary file.
        """

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
        """
        List book summaries.
        """

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

    def update(self, request, summary_id):
        """
        Update book summary.
        """

        try:
            bookSummary = self.get_queryset().filter(id=summary_id)
        except BookSummary.DoesNotExist:
            return Response(
                "Book summary not found", status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(bookSummary, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, summary_id):
        """
        Delete book summary.
        """

        try:
            bookSummary = self.get_queryset().filter(id=summary_id)
        except BookSummary.DoesNotExist:
            return Response(
                "Book summary not found", status=status.HTTP_400_BAD_REQUEST
            )
        bookSummary.delete()
        return Response("Summary deleted", status=status.HTTP_204_NO_CONTENT)


class BookSummaryDownload(viewsets.ModelViewSet):
    """Download book summary pdf"""

    def download_book_summary_pdf(self, request, book_summary_id):
        """Download book summary pdf"""

        book_summary = get_object_or_404(BookSummary, id=book_summary_id)
        if book_summary.summary:
            response = FileResponse(
                book_summary.summary.open("rb"),
                as_attachment=False,
                filename=book_summary.summary.name,
            )
            return response
        else:
            return HttpResponseNotFound(
                "The requested book summary does not have a PDF file."
            )
