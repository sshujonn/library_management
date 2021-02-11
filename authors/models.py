from django.db import models

# Create your models here.

class Author(models.Model):

    profile = models.OneToOneField('users.Profile', on_delete=models.CASCADE)
    anonym = models.CharField(max_length=255)
    # ToDo Add more fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.profile