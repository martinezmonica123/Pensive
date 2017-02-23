from django import forms
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags' )
        labels = {'title': 'Title', 'body': 'Body', 'tags': 'Tags'}


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ( 'image', 'tags' )
        labels = { 'tags': 'Tags'}
