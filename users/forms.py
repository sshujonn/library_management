from django import forms


class SignUpForm(forms.Form):
    fullname = forms.CharField()
    address = forms.CharField(required=False)
    gender = forms.IntegerField(required=False)
    image = forms.ImageField(required=False)
    phone_no = forms.CharField(required=False)


class EmailSignUpForm(SignUpForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)


class EmailSignInForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class CreateGroupForm(forms.Form):
    name = forms.CharField()

class AuthorizeUserForm(forms.Form):
    user_id = forms.IntegerField(required=True)
    is_library_admin = forms.BooleanField(required=False)