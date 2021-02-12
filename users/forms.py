from django import forms


class SignUpForm(forms.Form):
    fullname = forms.CharField()
    address = forms.CharField(required=False)
    gender = forms.IntegerField(required=False)
    image = forms.CharField(required=False)
    phone_no = forms.CharField(required=False)


class EmailSignUpForm(SignUpForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
