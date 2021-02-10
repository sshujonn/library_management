from django.db import models
# Create your models here.

class Books(models.Model):
    name = models.CharField(max_length=250)
    author_id = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    cover_image = models.ImageField(null=True, upload_to='static/img/cover_image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
