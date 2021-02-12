from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from users.forms import EmailSignUpForm, EmailSignInForm
from users.service import ProfileService


# Create your views here.
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def email_signup(request):
    try:

        form = EmailSignUpForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            email = form.cleaned_data["email"]
            data["username"] = email

            response = ProfileService().create_profile(data)
            if response.get("id"):
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Bad Request", "data": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def email_signin(request):
    try:

        form = EmailSignInForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            result = ProfileService().get_user_by_email(email, password)
            if not result:
                return Response({"detail": "Please check your credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"detail": "Success", "data": result}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Bad Request", "data": form.errors}, status=status.HTTP_400_BAD_REQUEST)


    except Exception as ex:

        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


