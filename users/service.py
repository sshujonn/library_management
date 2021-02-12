from rest_framework import serializers

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
                password=data["password"],
                fullname=data["fullname"],
                address=data["address"],
                gender=data["gender"] if data["gender"] else 1,
                image=data["image"],
                phone_no=data["phone_no"]
            )
            setattr(profile, "is_active", False)

            profile.save()
            serializer = ProfileSerializer(profile)
            return serializer.data
        else:
            return {"message": "Already Exists"}


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
