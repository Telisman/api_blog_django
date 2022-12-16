from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("id","username", "password1", "password2")

class AddBlog(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'owner')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(
                attrs={'class': 'form-control', 'value': '', 'id': 'user', 'type': 'hidden'}),
        }