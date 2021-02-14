import json
from django.core.paginator import Paginator
from rest_framework import serializers

from authors.models import Author
from library_management import config
from users.models import Profile
from users.service import ProfileSerializer


class AuthorsService:
    def browse_authors(self, page_no):
        try:
            authors = Author.objects.all()
            paginator = Paginator(authors, config.PAGE_SIZE)  # Show config.PAGE_SIZE contacts per page.
            page_authors = paginator.get_page(page_no)
            result = {
                "has_next": page_authors.has_next(),
                "has_previous": page_authors.has_previous()
            }
            author_list = json.dumps(AuthorSerializer(page_authors.object_list, many=True).data)
            result["data"] = json.loads(author_list)
            return result
        except:
            return False

    def create_author(self, data):
        try:
            author = Author.objects.filter(profile_id=data["profile"])[:1].get()
        except:
            author = None
        try:
            if author is None:
                profile = Profile.objects.get(pk=data["profile"])
                setattr(profile, "is_authorized", True)
                profile.save()
                author = Author(
                    profile=profile,
                    anonym=data["anonym"]
                )
                author.save()
                serializer = AuthorSerializer(author)
                return serializer.data
            else:
                return {"message": "Already Exists"}
        except:
            return {"error_code": 404}

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
