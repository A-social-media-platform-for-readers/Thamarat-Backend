from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
class AccountStatus(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class Member(models.Model):
    # common fields
    # Member_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=55, choices=AccountStatus)

    # specific fields for reader and author
    birth_date = models.DateField(default=None)
    gender = models.CharField(max_length=55, choices=Gender, default="M")

    # specific fields for publisher
    phone = models.CharField(max_length=20, default=None)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, default=None)

    #identity
    #dataofmembership