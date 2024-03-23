from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    readers_count = models.PositiveIntegerField(default=0)
    to_read_count = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to="media/book_covers/", default=None)
    pdf_file = models.FileField(upload_to="media/pdf_files/", default=None)

    def __str__(self):
        return self.title
