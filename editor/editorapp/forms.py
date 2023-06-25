from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Note, Snippet



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]


    
class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ["title", "text"]


class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        fields = ["title", "code", "language", "style", "context"]

