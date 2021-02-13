from rest_framework import status, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from books.forms import CreateBookForm, UpdateBookForm, DeleteBookForm, CreateBookLoanForm, UpdateBookLoanForm, CreateCategoryForm
from books.service import BooksService, BookLoanService, CategoryService
from library_management import config


# Create your views here.

@api_view(['GET'])
def browse_books(request):
    try:
        page_number = request.GET.get("page_no")
        response = BooksService().browse_books(page_number)
        if response:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something happened wrong!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def create_book(request):
    try:
        form = CreateBookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = BooksService().create_book(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                elif response.get("error_code") == 404:
                    return Response({"detail": "Invalid Author"},
                                    status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid Value"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_book(request):
    try:

        form = UpdateBookForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = BooksService().update_book(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid Value"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def delete_book(request):
    try:
        form = DeleteBookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = BooksService().delete_book(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid Value"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def browse_book_loans(request):
    try:
        page_number = request.GET.get("page_no")
        response = BookLoanService().browse_book_loans(page_number, request.user)
        if response:
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Something happened wrong!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_book_loan(request):
    try:
        form = CreateBookLoanForm(request.POST)
        if form.is_valid():
            member = request.user.groups.filter(name=config.MEMBER)
            if len(member)>0:
                data = form.cleaned_data
                data["profile_id"] = request.user.id
                response = BookLoanService().create_book_loan(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({"message": "Invalid Value"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_book_loan(request):
    try:
        form = UpdateBookLoanForm(request.POST)
        if form.is_valid():
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if len(library_admin)>0 or request.user.is_superuser:
                data = form.cleaned_data
                response = BookLoanService().update_book_loan(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_409_CONFLICT)

            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({"message": "Invalid Value"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_category(request):
    try:
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = CategoryService().create_category(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message": "Invalid Value"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
