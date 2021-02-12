import os
import requests

from django.contrib.auth.models import User
from oauth2_provider.models import Application
import random,string


class DefaultService():
    def access_token(self, client_id, client_secret, username, password, grant_type="password", scope=None):
        payload = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password
        }

        if scope is not None:
            payload['scope'] = scope

        try:
            base_url = os.getenv('SCHEMA_URL', 'http://localhost:8000/')
            url = base_url + 'o/token/'
            response = requests.post(url, data=payload).json()
        except Exception as ex:
            return False, str(ex)

        return True, response

    def create_super_user(self):
        user = User.objects.create_user(username='admin',
                                        email='admin@gmail.com',
                                        password='admin123')

        user.is_superuser = True

        user.save()

        return user

    def create_oath2_application(self, user_id):
        application = Application(
            name="library_management",
            client_id="c8fO42qEIvtn2NkHyBAmOwOHnQCYaAlkUTAZHBZW",
            client_secret="SbkpN6VebOsjMKDaGYuEnquKwQwohi1UGdNmGdofUQbXI88cLuv6qqrCroDRYMuDKY8IJlQgOQQdctn6YRrOfcdbclfxeVTrkXfCw0AUPKliF35FNbGdfQ03IYHxSYQ3",
            client_type="confidential",
            authorization_grant_type="password",
            user_id=user_id
        )

        application.save()

        return application

    def random_token_generator(self):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(30))
