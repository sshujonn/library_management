import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.service import DefaultService

default_service = DefaultService()


class test_profile(APITestCase):
    def setUp(self):
        super_user, password = default_service.create_super_user()
        self.application = default_service.create_oath2_application(super_user.id)
        self.content_type = "application/x-www-form-urlencoded"
        self.username = super_user.username
        self.password = password

    def create_profile(self):
        url = reverse('EmailSignUp')
        body = {
            "email": self.username,
            "password": self.password,
            "fullname": "User",
            "address": "Jessore",
            "phone_no": "01727711899"
        }
        response = self.client.post(url, body, CONTENT_TYPE=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['username'], self.username)
        self.assertEqual(data['fullname'], data['fullname'])

    def get_access_token(self):
        url = reverse('oauth2_provider:token')
        body = {
            "username": self.username,
            "password": self.password,
            "grant_type": self.application.authorization_grant_type,
            "client_id": self.application.client_id,
            "client_secret": self.application.client_secret,
        }
        response = self.client.post(url, body, CONTENT_TYPE=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = (json.loads(response.content))
        self.assertEqual(data['token_type'], 'Bearer')
        return data

    def create_group(self, oath2_token):
        url = reverse('CreateGroup')
        authorization = oath2_token["token_type"] + ' ' + oath2_token["access_token"]
        data = {'name' : 'library_admin'}
        response = self.client.post(url,data, CONTENT_TYPE=self.content_type, HTTP_AUTHORIZATION=authorization)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = (json.loads(response.content))
        self.assertEqual(data['name'], response['name'])

    def test_create_group(self):
        oath2_token = self.get_access_token()
        self.create_group(oath2_token)

    def sign_up(self):
        url = reverse('EmailSignUp')
        body = {
            "email": 'library_admin@gmail.com',
            "password": 'admin123',
            "fullname": "library_admin",
            "address": "Jessore",
            "phone_no": "01727711899"
        }
        response = self.client.post(url, body, CONTENT_TYPE=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['username'], body['email'])
        self.assertEqual(data['fullname'], body['fullname'])
        return data

    def authorize_user(self, oath2_token):

        url = reverse('AuthorizeUser')
        authorization = oath2_token["token_type"] + ' ' + oath2_token["access_token"]
        data = {'user_id':2,'is_library_admin':True}
        response = self.client.post(url,data, CONTENT_TYPE=self.content_type, HTTP_AUTHORIZATION=authorization)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = (json.loads(response.content))
        self.assertEqual(True, response['is_authorized'])

    def test_signup_authorize_user(self):
        oath2_token = self.get_access_token()
        self.sign_up()
        self.create_group(oath2_token)
        self.authorize_user(oath2_token)

