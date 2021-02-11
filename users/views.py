from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from users.forms import EmailSignUpForm
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
                return Response(response, status = status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    except Exception as ex:
        return Response({"message": "Something happened wrong!", "data": ex},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
