from django import forms


class CreateBookForm(forms.Form):
    name = forms.CharField(required=True)
    cover_image = forms.CharField(required=False)
    category_id = forms.IntegerField(required=True)


class UpdateBookForm(forms.Form):
    id = forms.IntegerField(required=True)
    name = forms.CharField(required=False)
    cover_image = forms.CharField(required=False)
    category_id = forms.IntegerField(required=False)


class DeleteBookForm(forms.Form):
    id = forms.IntegerField(required=True)


class CreateBookLoanForm(forms.Form):
    book_id = forms.IntegerField(required=True)
    request_type = forms.IntegerField(required=True)

class UpdateBookLoanForm(forms.Form):
    loan_id = forms.IntegerField(required=True)
    action = forms.IntegerField(required=True)

class CreateCategoryForm(forms.Form):
    name = forms.CharField(required=False)