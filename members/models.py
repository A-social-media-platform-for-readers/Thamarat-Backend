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


class Reader(models.Model):
    Reader_id = models.BigAutoField(primary_key=True)
    reader_birth_date = models.DateField()
    reader_gender = models.CharField(max_length=55, choices=Gender, default="M")


class Author(models.Model):
    author_id = models.BigAutoField(primary_key=True)
    author_birth_date = models.DateField()
    author_gender = models.CharField(max_length=55, choices=Gender, default="M")


class PublishingHouse(models.Model):
    publishing_house_id = models.BigAutoField(primary_key=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)


class Member(Reader, Author, PublishingHouse):
    Member_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=55 ,choices=AccountStatus)
    dateOfMembership = models.DateTimeField(auto_now_add=True)
    identity = models.CharField(
        choices=(
            ("reader", "Reader"),
            ("author", "Author"),
            ("publishingHouse", "PublishingHouse"),
        ),
        
max_length=255,
    )

