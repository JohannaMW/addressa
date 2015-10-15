from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from app.models import Client, AccountContact


class AccountContactForm(ModelForm):
    class Meta:
        model = AccountContact
        fields = ("first_name", "last_name", "email", "company", "phone")


class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Client
        fields = ("username", "email", "password1", "password2")

class UpdateProfile(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Client
        fields = ("username", "first_name", "last_name", "email", "website", "company", "password1", "password2")

#clean email field
def clean_email(self):
    email = self.cleaned_data["email"]
    try:
        Client._default_manager.get(email=email)
    except Client.DoesNotExist:
        return email
    raise forms.ValidationError('duplicate email')

#modify save() method so that we can set user.is_active to False when we first create our user
def save(self, commit=True):
    user = super(ClientRegistrationForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.is_active = False # not active until he opens activation link
        user.save()

    return user