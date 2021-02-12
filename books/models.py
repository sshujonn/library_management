from django.db import models

from authors.models import Author
from users.models import Profile


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)


class Books(models.Model):
    name = models.CharField(max_length=250)
    cover_image = models.ImageField(null=True, upload_to='static/img/cover_image')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)

    authors = models.ManyToManyField(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookLoan(models.Model):
    STATUS_CHOICES = (
        (1, "Requested"),
        (2, "Taken"),
        (3, "Returned")
    )
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default="1", blank=True)
