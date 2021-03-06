from django import forms

from .models import BookLoan

class CreateBookForm(forms.Form):
    name = forms.CharField(required=True)
    cover_image = forms.ImageField(required=False)
    category_id = forms.IntegerField(required=True)
    authors = forms.CharField(required=True)


class UpdateBookForm(forms.Form):
    id = forms.IntegerField(required=True)
    name = forms.CharField(required=False)
    cover_image = forms.ImageField(required=False)
    category_id = forms.IntegerField(required=False)


class DeleteBookForm(forms.Form):
    id = forms.IntegerField(required=True)


class CreateBookLoanForm(forms.Form):
    book_id = forms.IntegerField(required=True)
    request_type = forms.IntegerField(required=True)


class UpdateBookLoanForm(forms.ModelForm):
    class Meta:
        model = BookLoan
        fields = (
            'id',
            'status'
        )


class ExportBookLoanForm(forms.Form):
    status = forms.IntegerField(required=False)


class CreateCategoryForm(forms.Form):
    name = forms.CharField(required=False)
