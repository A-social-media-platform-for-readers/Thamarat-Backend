from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# class AccountStatus(models.TextChoices):
#     ACTIVE = "ACTIVE"
#     INACTIVE = "INACTIVE"


class Gender(models.TextChoices):
    """
    Gender choices for user
    """

    MALE = "M", "Male"
    FEMALE = "F", "Female"


class Identity(models.TextChoices):
    """
    Identity choices for user
    """

    READER = "READER"
    AUTHOR = "AUTHOR"
    PUBLISHER = "PUBLISHER"


class Address(models.Model):
    """
    Address model for user
    """

    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255, blank=True)
    # city = models.CharField(max_length=255, blank=True)
    # state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)


class User(AbstractUser):
    """
    User override model for authentication
    """

    id = models.AutoField(primary_key=True)
    identity = models.CharField(max_length=55, choices=Identity)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to="media/profile_images/", blank=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    following = models.ManyToManyField(
        "self", related_name="i_follow", symmetrical=False, blank=True
    )
    # specific fields for reader and author
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=55, choices=Gender, blank=True)

    # specific fields for publisher
    phone = models.CharField(max_length=20, blank=True)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, blank=True, null=True
    )

    # django depend on username in authentication process but
    # we want to depend on email in authentication process
    # because email is unique field
    # so we have to manually set username field to email
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
