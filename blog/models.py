from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

def get_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return 'post-images/%s-%s' % (slug, filename)

class Image(models.Model):
    #owner = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_added = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to=get_filename, verbose_name='Images')
    tags = TaggableManager()
