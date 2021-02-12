"""library_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from authors import views as author_view
from books import views as book_view
from users import views as user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'email-signup', user_view.email_signup, name="EmailSignUp"),
    url(r'email-signin', user_view.email_signin, name="EmailSignIn"),

    url(r'create-book', book_view.create_book, name="CreateBook"),
    url(r'update-book', book_view.update_book, name="UpdateBook"),
    url(r'delete-book', book_view.delete_book, name="DeleteBook"),

    url(r'create-author', author_view.create_author, name="CreateAuthor"),
    url(r'update-author', author_view.update_author, name="UpdateAuthor"),
    url(r'delete-author', author_view.delete_author, name="DeleteAuthor"),
]
