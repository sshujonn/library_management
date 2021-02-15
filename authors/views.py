from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from authors.forms import CreateAuthorForm, UpdateAuthorForm, DeleteAuthorForm
from authors.service import AuthorsService
from library_management import config


# Create your views here.
#TODO:: Create and user decorator as response status are same.
@api_view(['GET'])
def browse_authors(request):
    """
        Functionality: Browse authors
        Params: page_no (optional)
        Response: authors list
    """
    try:
        page_number = request.GET.get("page_no")
        response = AuthorsService().browse_authors(page_number)
        if response:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something happened wrong!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_author(request):
    """
        Functionality: create a author
        Params: author info
        Response: created author
    """
    try:
        form = CreateAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = AuthorsService().create_author(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                elif response.get("error_code"):
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid Value"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_author(request):
    """
        Functionality: update a author
        Params: author info
        Response: updated author
    """
    try:

        form = UpdateAuthorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = AuthorsService().update_author(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def delete_author(request):
    """
        Functionality: delete a author
        Params: author id
        Response: deleted author info
    """
    try:
        form = DeleteAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = AuthorsService().delete_author(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
