from django import forms


class CreateBookForm(forms.Form):
    name = forms.CharField(required=True)
    cover_image = forms.CharField(required=False)


class UpdateBookForm(forms.Form):
    id = forms.IntegerField(required=True)
    name = forms.CharField(required=False)
    cover_image = forms.CharField(required=False)


class DeleteBookForm(forms.Form):
    id = forms.IntegerField(required=True)
