from rest_framework import serializers

from authors.models import Author
from users.models import Profile
from users.service import ProfileSerializer

class AuthorsService:
    def create_author(self, data):
        try:
            author = Author.objects.filter(profile_id=data["profile"])[:1].get()
        except:
            author = None
        if author is None:
            author = Author(
                profile=Profile.objects.get(pk=data["profile"]),
                anonym=data["anonym"]
            )
            author.save()
            serializer = AuthorSerializer(author)
            return serializer.data
        else:
            return {"message": "Already Exists"}


    def update_author(self, data):
        try:
            author = Author.objects.get(pk=data["id"])
        except:
            author = None
        if author is not None:
            setattr(author, "anonym", data["anonym"])
            author.save()
            serializer = AuthorSerializer(author)
            return serializer.data
        else:
            return {"message": "Invalid author id"}


    def delete_author(self, data):
        try:
            author = Author.objects.get(pk=data["id"])
        except:
            author = None
        if author is not None:
            serializer = AuthorSerializer(author).data
            author.delete()
            return serializer
        else:
            return {"message": "Invalid author id"}

class AuthorSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(serializers.ModelSerializer)
    class Meta:
        model = Author
        fields = (
            'id',
            'profile',
            'anonym',
            'updated_at'
        )