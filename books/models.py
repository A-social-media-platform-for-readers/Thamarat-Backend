from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    """
    Model representing a book.

    Methods:
        __str__(): Returns the title of the book.
    """

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
    )
    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
        default=0,
    )
    genre = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    readers_count = models.PositiveIntegerField(default=0)
    to_read_count = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to="media/book_covers/", default=None)
    pdf_file = models.FileField(upload_to="media/pdf_files/", default=None)

    def __str__(self):
        """
        Returns the title of the book.
        """

        return self.title


class BookSummary(models.Model):
    """
    Model representing a summary of a book.
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    summary = models.FileField(upload_to="media/summary_files/", default=None)
