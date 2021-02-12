from rest_framework import serializers
from oauth2_provider.models import AccessToken, RefreshToken, Application
from datetime import datetime, timedelta

from library_management import config
from library_management.settings import OAUTH2_PROVIDER
from users.default import DefaultService
from users.models import Profile


class ProfileService(DefaultService):
    def create_profile(self, data):
        try:
            profile = Profile.objects.filter(email=data["email"])[:1].get()
        except:
            profile = None

        if profile is None:
            profile = Profile(
                email=data["email"],
                username=data["username"],
                fullname=data["fullname"],
                address=data["address"],
                gender=data["gender"] if data["gender"] else 1,
                image=data["image"],
                phone_no=data["phone_no"]
            )
            profile.set_password(data["password"])
            setattr(profile, "is_active", False)

            profile.save()
            serializer = ProfileSerializer(profile)
            return serializer.data
        else:
            return {"message": "Already Exists"}


    def get_user_by_email(self, email, password):
        try:
            user = Profile.objects.filter(email=email)[:1].get()
        except:
            return False
        if user.check_password(password):
            if user.is_active is False:
                user.is_active = True
                user.save()
        else:
            return False

        result = ProfileSerializer(user).data
        try:
            access_token = AccessToken.objects.filter(user=user).latest('expires')
            refresh_token = RefreshToken.objects.filter(access_token=access_token).latest('created')
        except:
            access_token = None
            refresh_token = None
        if  access_token is None or access_token.expires.replace(tzinfo=None) < datetime.now():
            try:
                application = Application.objects.get(name=config.APP_NAME)
                expiry = datetime.now() + timedelta(seconds=OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
                scopes = "read write groups"
                access_token = AccessToken.objects.create(user=user, application=application,
                                                          token=self.random_token_generator(), expires=expiry,
                                                          scope=scopes)
                refresh_token=RefreshToken.objects.create(user=user, token=self.random_token_generator(),
                                            access_token=access_token, application=application)
            except Exception as ex:
                result["exp"] = str(ex)


        if access_token is not None and refresh_token is not None:
            try:
                result["access_token"] = access_token.token
                result["token_type"] = "Bearer"
                result["scope"] = access_token.scope
                result["expires"] = access_token.expires
                result["refresh_token"] = refresh_token.token
            except Exception as ex:
                result["exp"] = str(ex)

        return result




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'email',
            'fullname',
            'address',
            'phone_no',
            'image',
            'gender',
            'updated_at'
        )
