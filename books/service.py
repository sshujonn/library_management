from django.core.paginator import Paginator

from rest_framework import serializers
import json

from library_management import config

from books.models import Books, BookLoan, Category
from users.models import Profile

from users.service import ProfileSerializer


class BooksService:

    def browse_books(self,page_no):
        try:
            books = Books.objects.all()
            paginator = Paginator(books, config.PAGE_SIZE)  # Show config.PAGE_SIZE contacts per page.
            page_books = paginator.get_page(page_no)
            result = {
                "has_next" : page_books.has_next(),
                "has_previous": page_books.has_previous()
            }
            book_list = json.dumps(BookSerializer(page_books.object_list, many=True).data)
            # import pdb;pdb.set_trace()
            result["data"] = json.loads(book_list)
            return result
        except:
            return False


    def create_book(self, data):
        try:
            book = Books.objects.filter(name=data["name"])[:1].get()
        except:
            book = None
        if book is None:
            book = Books(
                name=data["name"],
                cover_image=data["cover_image"],
                category = Category.objects.get(pk=data["category_id"])
            )
            book.save()
            # import  pdb;pdb.set_trace()
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
            setattr(book, "name", data["name"]) if "name" in data  else ''
            setattr(book, "cover_image", data["cover_image"]) if "cover_image" in data  else ''
            setattr(book, "category_id", data["category_id"]) if "category_id" in data  else ''
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

class BookLoanService:
    def create_book_loan(self, data):
        try:
            #TODO add profile_id to the filter
            book_loan = BookLoan.objects.filter(book_id=data["book_id"], profile_id=data["profile_id"])[:1].get()
        except:
            book_loan = None
        #check if the book is taken or pending by the user already.
        #Loan request can only be created if same book is neither taken or requested by same user
        taken_pending_status = [1,2] #Todo avoid magic number
        # import pdb;pdb.set_trace()
        if book_loan is None and data["request_type"]==1:
            book_loan = BookLoan(
                profile=Profile.objects.get(pk=data["profile_id"]),
                book=Books.objects.get(pk=data["book_id"]),
                request_type = data["request_type"] #Todo avoid magic number
            )
            book_loan.save()
            serializer = BookLoanSerializer(book_loan)
            return serializer.data

        elif book_loan and book_loan.status not in taken_pending_status:
            setattr(book_loan, "status", 1)
            setattr(book_loan, "request_type", data["request_type"])
            book_loan.save()
            serializer = BookLoanSerializer(book_loan)
            return serializer.data

        elif book_loan is not None and data["request_type"]==2:
            # check if the book is returned by the user already
            if book_loan.status != 3: #Todo avoid magic number
                setattr(book_loan, "status", 1)
                setattr(book_loan, "request_type", data["request_type"])
            else:
                return {"message": "Already returned"}
            book_loan.save()
            serializer = BookLoanSerializer(book_loan)
            return serializer.data
        else:
            return {"message": "Invalid request"}


    def update_book_loan(self, data):
        try:
            #TODO add profile_id to the filter
            book_loan = BookLoan.objects.filter(pk=data["loan_id"])[:1].get()
        except:
            book_loan = None
        #check if the loan request is pending
        # import pdb;pdb.set_trace()
        if book_loan and book_loan.status==1:#Todo avoid magic number
            setattr(book_loan,"status", data["action"])
            book_loan.save()
            serializer = BookLoanSerializer(book_loan)
            return serializer.data
        else:
            return {"message": "Invalid request"}


class CategoryService:
    def create_category(self, data):
        try:
            category = Category.objects.filter(name=data["name"])[:1].get()
        except:
            category = None
        if category is None:
            category = Category(
                name=data["name"]
            )
            category.save()
            serializer = CategorySerializer(category)
            return serializer.data
        else:
            return {"message": "Already Exists"}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(serializers.ModelSerializer)
    class Meta:
        model = Books
        fields = (
            'id',
            'name',
            'category',
            'cover_image',
            'updated_at'
        )


class BookLoanSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(serializers.ModelSerializer)
    book = BookSerializer(serializers.ModelSerializer)
    class Meta:
        model = BookLoan
        fields = (
            'id',
            'profile',
            'book',
            'status',
            'updated_at'
        )
