from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(User):
    GENDER_CHOICES = (
        (1, "Male"),
        (2, "Female"),
        (3, "Other")
    )

    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=50, blank=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default="1", blank=True)
    image = models.ImageField(null=True, upload_to='static/img/profile_image')
    is_authorized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
