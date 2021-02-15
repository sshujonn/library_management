import datetime
import json
from django.core.paginator import Paginator
from djqscsv import write_csv
from rest_framework import serializers

from authors.models import Author
from books.models import Books, BookLoan, Category
from library_management import config
from library_management.settings import EXPORT_REPORT_URL, ROOT_PATH
from users.models import Profile
from users.service import ProfileSerializer


class BooksService:

    def browse_books(self, page_no):
        try:
            books = Books.objects.all()
            paginator = Paginator(books, config.PAGE_SIZE)  # Show config.PAGE_SIZE contacts per page.
            page_books = paginator.get_page(page_no)
            result = {
                "has_next": page_books.has_next(),
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
            try:
                book = Books(
                    name=data["name"],
                    cover_image=data["cover_image"],
                    category=Category.objects.get(pk=data["category_id"])
                )
                authors_list = list()
                authors = data["authors"].split(",")
                for author_id in authors:
                    author = Author.objects.get(pk=author_id)
                    authors_list.append(author)
                book.save()
                book.authors.add(*authors_list)
                # import  pdb;pdb.set_trace()
                serializer = BookSerializer(book)
                return serializer.data
            except:
                return {"error_code": 404, "message": "Invalid Author/Category"}

        else:
            return {"message": "Already Exists"}

    def update_book(self, data):
        try:
            book = Books.objects.get(pk=data["id"])
        except:
            book = None
        if book is not None:
            # import pdb;pdb.set_trace()
            setattr(book, "name", data["name"]) if "name" in data else book.name
            setattr(book, "cover_image", data["cover_image"]) if data.get("cover_image") else book.cover_image
            setattr(book, "category_id", data["category_id"]) if data.get("category_id") else book.category_id
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

    def browse_book_loans(self, page_no, user):
        try:
            member = user.groups.filter(name=config.MEMBER)
            if len(member) > 0:
                book_loans = BookLoan.objects.filter(profile_id=user.id, status=1)# show only pending book loan request
            else:
                book_loans = BookLoan.objects.filter(status=1) # show only pending book loan request
            paginator = Paginator(book_loans, config.PAGE_SIZE)  # Show config.PAGE_SIZE contacts per page.
            page_book_loans = paginator.get_page(page_no)
            result = {
                "has_next": page_book_loans.has_next(),
                "has_previous": page_book_loans.has_previous()
            }
            book_list = json.dumps(BookLoanSerializer(page_book_loans.object_list, many=True).data)
            # import pdb;pdb.set_trace()
            result["data"] = json.loads(book_list)
            return result
        except:
            return False

    def create_book_loan(self, data):
        try:
            # TODO add profile_id to the filter
            book_loan = BookLoan.objects.filter(book_id=data["book_id"], profile_id=data["profile_id"])[:1].get()
        except:
            book_loan = None
        # check if the book is taken or pending by the user already.
        # Loan request can only be created if same book is neither taken or requested by same user
        taken_pending_status = [1, 2]  # Todo avoid magic number
        # import pdb;pdb.set_trace()
        if book_loan is None and data["request_type"] == 1:
            try:
                book_loan = BookLoan(
                    profile=Profile.objects.get(pk=data["profile_id"]),
                    book=Books.objects.get(pk=data["book_id"]),
                    request_type=data["request_type"]  # Todo avoid magic number
                )
                book_loan.save()
                serializer = BookLoanSerializer(book_loan)
                return serializer.data
            except:
                return {"message": "Invalid Book"}

        elif book_loan and book_loan.status not in taken_pending_status:
            setattr(book_loan, "status", 1)
            setattr(book_loan, "request_type", data["request_type"])
            book_loan.save()
            serializer = BookLoanSerializer(book_loan)
            return serializer.data

        elif book_loan is not None and data["request_type"] == 2:
            # check if the book is returned by the user already
            if book_loan.status != 3:  # Todo avoid magic number
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
            # TODO add profile_id to the filter
            book_loan = BookLoan.objects.filter(pk=data["id"])[:1].get()
        except:
            book_loan = None
        # check if the loan request is pending
        # import pdb;pdb.set_trace()
        if book_loan and book_loan.status == 1:  # Todo avoid magic number
            setattr(book_loan, "status", data["status"])
            book_loan.save()
            serializer = BookLoanSerializer(book_loan)
            return serializer.data
        else:
            return {"message": "Invalid request"}

    def export_book_loan(self, data):
        # getting report path declared in settings
        base_path = EXPORT_REPORT_URL
        # Initial file name
        file_name = "export_book_loan_"
        try:
            # this if else block defines if the report will be for specific status of loan or for all
            if data.get("status"):
                queryset = BookLoan.objects.filter(status=data["status"])
                file_name += str(data.get("status")) + "_"
            else:
                queryset = BookLoan.objects.all()
                file_name += "all_"

            # adding timestamp to file name to make unique file name
            timestamp = round(datetime.datetime.now().timestamp())
            file_name += str(timestamp) + ".csv"
            file_path = base_path + file_name
            with open(file_path[1:], 'wb') as csv_file:
                write_csv(queryset, csv_file)
            return {"file_path": file_path}
        except:
            return {"error": "Invalid Book Loan Data or file generation failed"}


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
