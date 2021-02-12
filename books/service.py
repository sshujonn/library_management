from rest_framework import serializers

from books.models import Books


class BooksService:
    def create_book(self, data):
        try:
            book = Books.objects.filter(name=data["name"])[:1].get()
        except:
            book = None
        if book is None:
            book = Books(
                name=data["name"],
                cover_image=data["cover_image"]
            )
            book.save()
            serializer = BookSerializer(book)
            return serializer.data
        else:
            return {"message": "Already Exists"}

    def update_book(self, data):
        try:
            book = Books.objects.get(pk=data["id"])
        except:
            book = None
        if book is not None:
            setattr(book, "name", data["name"])
            setattr(book, "cover_image", data["cover_image"])
            book.save()
            serializer = BookSerializer(book)
            return serializer.data
        else:
            return {"message": "Invalid book id"}

    def delete_book(self, data):
        try:
            book = Books.objects.get(pk=data["id"])
        except:
            book = None
        if book is not None:
            serializer = BookSerializer(book).data
            book.delete()
            return serializer
        else:
            return {"message": "Invalid book id"}


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = (
            'id',
            'name',
            'cover_image',
            'updated_at'
        )
