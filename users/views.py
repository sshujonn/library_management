from rest_framework import status, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from library_management import config
from users.forms import EmailSignUpForm, EmailSignInForm, CreateGroupForm, AuthorizeUserForm
from users.models import Profile
from users.service import ProfileService


# Create your views here.
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def email_signup(request):
    """
        Functionality: signup for all types of users
        Params: user info
        Response: user info
    """
    try:
        form = EmailSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            email = form.cleaned_data["email"]
            data["username"] = email

            response = ProfileService().create_profile(data)
            if response.get("id"):
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"detail": "Bad Request", "data": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def email_signin(request):
    """
        Functionality: signin for all types of users
        Params: username, password
        Response: access token
    """
    try:

        form = EmailSignInForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            result = ProfileService().get_user_by_email(email, password)
            if not result:
                return Response({"detail": "invalid credentials or unauthorized user"},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({"detail": "Success", "data": result}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Bad Request", "data": form.errors}, status=status.HTTP_400_BAD_REQUEST)


    except Exception as ex:

        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# To Create Group through API, Can be created from admin panel either
@api_view(['POST'])
def create_group(request):
    """
        Functionality: user group creation
        Params: group name
        Response: group
    """
    form = CreateGroupForm(request.POST)
    try:
        if form.is_valid():
            name = form.cleaned_data["name"]
            if request.user.is_superuser:
                response = ProfileService().create_group(name)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Bad Request", "data": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def authorize_user(request):
    """
        Functionality: Authorize a signed up user
        Params: user_id, is_library_admin
        Response: Success/Failure with profile
    """
    form = AuthorizeUserForm(request.POST)
    try:
        if form.is_valid():
            data = form.cleaned_data
            library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
            if request.user.is_superuser or len(library_admin) > 0:
                response = ProfileService().authorize_user(data)
                if response.get("id"):
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "Unauthorized Access"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Bad Request", "data": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def browse_unauthorized_users(request):
    """
        Functionality: shows unauthorized users
        Params: page_no (optional)
        Response: unauthorized users
    """
    try:
        library_admin = request.user.groups.filter(name=config.LIBRARY_ADMIN)
        if request.user.is_superuser or len(library_admin) > 0:
            page_number = request.GET.get("page_no")
            response = ProfileService().browse_unauthorized_users(page_number)
            if response:
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Something happened wrong!"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"detail": "Unauthorized Access"},
                            status=status.HTTP_401_UNAUTHORIZED)
    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

