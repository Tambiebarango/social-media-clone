from django import forms
from django.contrib.auth.models import User
from blogapp.models import UserProfileInfo, Post, Comment

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')
#connect specific widgets to classes/css files
        widgets = {
            'title':forms.TextInput(attrs={'class': 'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable mediumm-editor-textarea postcontent'})

        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class': 'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable mediumm-editor-textarea'})
            }
