from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import BookModel


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class BookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = ['name', 'author', 'publish', 'user']