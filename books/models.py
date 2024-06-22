from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    """
    Model representing a book.
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0.0
    )
    rate_users = models.ManyToManyField("users.User")
    total_rate = models.FloatField(default=0.0)
    rate_count = models.PositiveIntegerField(default=0)
    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10000)],
        default=0,
    )
    genre = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reviwes_count = models.PositiveIntegerField(default=0)
    readers_count = models.PositiveIntegerField(default=0)
    reading_count = models.PositiveIntegerField(default=0)
    to_read_count = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to="media/book_covers/", default=None)
    pdf_file = models.FileField(upload_to="media/pdf_files/", default=None)

    def __str__(self):
        """
        Returns the title of the book.
        """
        return self.title

    def calc_rate(self, rating):
        """
        Returns the total rate of the book.
        """
        if rating < 0 or rating > 5:
            raise ValueError("Invalid rating value")
        self.rate_count += 1
        self.total_rate = self.total_rate + rating
        self.rate = self.total_rate / self.rate_count
        self.save()

    def add_reviwe(self):
        """
        Add one to the number of reviwes.
        """
        self.reviwes_count += 1
        self.save()

    def remove_reviwe(self):
        """
        Remove one to the number of reviwes.
        """
        self.reviwes_count -= 1
        self.save()

    def add_reader(self):
        """
        Add one to the number of readers.
        """
        self.readers_count += 1
        self.save()

    def remove_reader(self):
        """
        Remove one to the number of readers.
        """
        self.readers_count -= 1
        self.save()

    def add_reading(self):
        """
        Add one to the number of readings.
        """
        self.reading_count += 1
        self.save()

    def remove_reading(self):
        """
        Remove one to the number of readings.
        """
        self.reading_count -= 1
        self.save()

    def add_to_read(self):
        """
        Add one to the number of want to read.
        """
        self.to_read_count += 1
        self.save()

    def remove_to_read(self):
        """
        Remove one to the number of want to read.
        """
        self.to_read_count -= 1
        self.save()


class BookSummary(models.Model):
    """
    Model representing a summary of a book.
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    summary = models.FileField(upload_to="media/summary_files/", default=None)


class BookReview(models.Model):
    """
    Model representing a review of a book.
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviewers"
    )
    content = models.TextField(max_length=1024)
    created_time = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Returns the title of the book.
        """
        return self.book.title

    class Meta:
        ordering = ["-like_count"]

    def like(self):
        """
        Add one to the number of likes.
        """
        self.like_count += 1
        self.save()

    def remove_like(self):
        """
        subtract one from the number of likes.
        """
        if self.like_count > 0:
            self.like_count -= 1
            self.save()


class BookReaders(models.Model):
    """
    Book readers users.
    """

    reader = models.ManyToManyField("users.User")
    book = models.ManyToManyField(Book)


class BookReading(models.Model):
    """
    Book Reading users.
    """

    reader = models.ManyToManyField("users.User")
    book = models.ManyToManyField(Book)


class BookToRead(models.Model):
    """
    Book want to read users.
    """

    reader = models.ManyToManyField("users.User")
    book = models.ManyToManyField(Book)
