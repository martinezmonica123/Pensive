import itertools

from django.utils.text import slugify
from django import forms
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags' )
        labels = {'title': 'Title', 'body': 'Body', 'tags': 'Tags'}

    def save(self):
        instance = super(PostForm, self).save(commit=False)

        max_length = Post._meta.get_field('slug').max_length
        instance.slug = orig = slugify(instance.title)[:max_length]

        for x in itertools.count(1):
            if not Post.objects.filter(slug=instance.slug).exists():
                break

            # Truncate the original slug dynamically. Minus 1 for the hyphen.
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        instance.save()
        return instance


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ( 'image', )
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'id_image"', 'required': True, 'placeholder': 'Say something...'}
            ),
        }
        #labels = { 'tags': 'Tags'}
