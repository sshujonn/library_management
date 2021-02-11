from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from books.forms import CreateBookForm, UpdateBookForm, DeleteBookForm
from books.service import BooksService

# Create your views here.
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def create_book(request):

    try:

        form = CreateBookForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            response = BooksService().create_book(data)
            if response.get("id"):
                return Response(response, status = status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid Value"},status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def update_book(request):

    try:

        form = UpdateBookForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            response = BooksService().update_book(data)
            if response.get("id"):
                return Response(response, status = status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid Value"},status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def delete_book(request):

    try:

        form = DeleteBookForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            response = BooksService().delete_book(data)
            if response.get("id"):
                return Response(response, status = status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid Value"},status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
