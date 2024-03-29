from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        blank=True,
        null=True,
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
        blank=True,
        null=True,
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
        return self.title
