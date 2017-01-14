from django.db import models
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=900)

    def __str__(self):
        return self.title

def get_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return 'post-images/%s-%s' % (slug, filename)

class Images(models.Model):
    post = models.ForeignKey(Post, default=None)
    image = models.ImageField(upload_to=get_filename, verbose_name='Image')
