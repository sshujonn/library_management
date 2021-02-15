# Register your models here.
from django.contrib import admin

from books.models import Books, BookLoan, Category

admin.site.register(Books)
admin.site.register(BookLoan)
admin.site.register(Category)