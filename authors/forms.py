from django import forms


class CreateAuthorForm(forms.Form):
    profile = forms.IntegerField(required=True)
    anonym = forms.CharField(required=False)


class UpdateAuthorForm(forms.Form):
    id = forms.IntegerField(required=True)
    anonym = forms.CharField(required=False)


class DeleteAuthorForm(forms.Form):
    id = forms.IntegerField(required=True)
