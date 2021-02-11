from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from authors.forms import CreateAuthorForm, UpdateAuthorForm, DeleteAuthorForm
from authors.service import AuthorsService

# Create your views here.
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def create_author(request):
    try:

        form = CreateAuthorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            # import pdb;pdb.set_trace()
            response = AuthorsService().create_author(data)
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
def update_author(request):

    try:

        form = UpdateAuthorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            response = AuthorsService().update_author(data)
            if response.get("id"):
                return Response(response, status = status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def delete_author(request):
    try:
        form = DeleteAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            response = AuthorsService().delete_author(data)
            if response.get("id"):
                return Response(response, status = status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
