from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.contrib.auth.models import Group, Permission
from oauth2_provider.models import AccessToken, RefreshToken, Application
from rest_framework import serializers
import json

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
        if user.check_password(password) and user.is_authorized:
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
        if access_token is None or access_token.expires.replace(tzinfo=None) < datetime.now():
            try:
                application = Application.objects.get(name=config.APP_NAME)
                expiry = datetime.now() + timedelta(seconds=OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])
                scopes = "read write groups"
                access_token = AccessToken.objects.create(user=user, application=application,
                                                          token=self.random_token_generator(), expires=expiry,
                                                          scope=scopes)
                refresh_token = RefreshToken.objects.create(user=user, token=self.random_token_generator(),
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

    def create_group(self, name):
        try:
            group = Group.objects.filter(name=name)[:1].get()
        except:
            group = None
        if group:
            return {"message": "Already Exists"}
        else:
            new_group = Group(
                name=name
            )
            new_group.save()
            serializer = GroupSerializer(new_group)
            return serializer.data

    def authorize_user(self, data):
        try:
            profile_id = data["user_id"]
            user = Profile.objects.get(pk=profile_id)
        except:
            user = None
        if not user:
            return {"message": "User doesn't Exist"}
        else:
            if "is_library_admin" in data and data["is_library_admin"]:
                group = Group.objects.get(name=config.LIBRARY_ADMIN)
            else:
                group = Group.objects.get(name=config.MEMBER)
            user.groups.add(group)
            setattr(user, "is_authorized", True)
            user.save()
            serializer = ProfileSerializer(user)
            return serializer.data

    def browse_unauthorized_users(self, page_no):
        try:
            unauth_members = Profile.objects.filter(is_authorized=False)
            paginator = Paginator(unauth_members, config.PAGE_SIZE)  # Show config.PAGE_SIZE contacts per page.
            page_unauth_members = paginator.get_page(page_no)
            result = {
                "has_next": page_unauth_members.has_next(),
                "has_previous": page_unauth_members.has_previous()
            }
            unauth_member_list = json.dumps(ProfileSerializer(page_unauth_members.object_list, many=True).data)
            result["data"] = json.loads(unauth_member_list)
            return result
        except:
            return False
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)


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
            'updated_at',
            'is_authorized'
        )
