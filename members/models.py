from django.db import models
from enum import Enum

"""
Unfortunately, directly inheriting from all the previous classes 
(Reader, Author, and PublishingHouse) is not possible in Django due 
to multiple inheritance limitations. However, depending on your needs,
you can achieve the desired functionality in several ways:

1. Union Model:

Create a new model Member that acts as a union of the three existing models.
This model would not have any additional fields but would inherit all the fields
and methods from the three parent models.

Python
class Member(models.Model):
    reader_ptr = models.OneToOneField(Reader, on_delete=models.CASCADE, null=True, blank=True)
    author_ptr = models.OneToOneField(Author, on_delete=models.CASCADE, null=True, blank=True)
    publishing_house_ptr = models.OneToOneField(
        PublishingHouse, on_delete=models.CASCADE, null=True, blank=True
        )

    def get_type(self):
        if self.reader_ptr:
            return "Reader"
        elif self.author_ptr:
            return "Author"
        elif self.publishing_house_ptr:
            return "PublishingHouse"
        else:
            raise ValueError("Invalid member type")
Use code with caution. Learn more
This approach allows you to query for members based on their type
(reader, author, or publishing house)
and access their specific fields and methods. However, it can be complex to
manage and may lead to redundant data if members share fields across roles.

2. Abstract Base Class:

Create an abstract base class MemberBase that inherits common fields and methods
like first_name, last_name, email, etc., and declare status and other relevant fields.
Then, create concrete models for Reader, Author, and PublishingHouse that inherit from
MemberBase and add their specific fields.

Python
class MemberBase(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=1, choices=AccountStatus.choices)

    class Meta:
        abstract = True

class Reader(MemberBase):
    reader_id = models.CharField(max_length=255, unique=True)
    # ... other reader fields

class Author(MemberBase):
    author_id = models.CharField(max_length=255, unique=True)
    # ... other author fields

class PublishingHouse(MemberBase):
    publishing_house_id = models.CharField(max_length=255, unique=True)
    # ... other publishing house fields

Use code with caution. Learn more
This approach provides a more organized structure and avoids data redundancy.
You can then query members based on their concrete model type and access their
specific fields and methods.

3. Role-based Permissions:

Instead of inheriting from all models, consider using a separate model for roles
and assigning roles to users based on their type. This allows for more flexibility
and granular control over permissions and access.

Ultimately, the best approach depends on your specific needs and the complexity of
your project. Carefully consider your requirements and choose the option that provides
the most efficient and maintainable solution.
"""


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


class Member(models.Model):
    Member_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=55, choices=AccountStatus.choices)
    dateOfMembership = models.DateTimeField(auto_now_add=True)


class Reader(Member):
    Reader_id = models.BigAutoField(primary_key=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=55, choices=Gender.choices)


class Author(Member):
    author_id = models.BigAutoField(primary_key=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=55, choices=Gender.choices)


class PublishingHouse(Member):
    publishing_house_id = models.BigAutoField(primary_key=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
