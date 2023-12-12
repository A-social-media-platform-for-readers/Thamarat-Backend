from django.db import models
from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class Address(models.Model):
    # street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class Reader(models.Model):
    Reader_id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=55)
    lastname = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=55, choices=Gender.choices)
    status = models.CharField(max_length=55, choices=AccountStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)


class Author(models.Model):
    author_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(max_length=55, choices=Gender.choices)
    status = models.CharField(max_length=55, choices=AccountStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)


class PublishingHouse(models.Model):
    publishing_house_id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=1, choices=AccountStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
