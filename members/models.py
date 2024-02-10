from django.db import models


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
    Member_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=55, choices=AccountStatus)
    dateOfMembership = models.DateTimeField(auto_now_add=True)
    identity = (
        ("reader", "Reader"),
        ("author", "Author"),
        ("publisher", "Publishing House"),
    )

    # specific fields for reader and author
    birth_date = models.DateField()
    gender = models.CharField(max_length=55, choices=Gender, default="M")

    # specific fields for publisher
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
