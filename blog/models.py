from django.db import models
from django.utils.text import slugify
#from slugify import slugify
from taggit.managers import TaggableManager


def get_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return 'post-images/%s-%s' % (slug, filename)


# Create your models here.
class Post(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)

    tags = TaggableManager()
    slug = models.SlugField(unique=True)

    # can't return tags as a list using TaggableManager try this instead:
    #
    # list_display = ['tag_list']
    #
    # def get_queryset(self, request):
    #     return super(models.Model, self).get_queryset(request).prefetch_related('tags')
    #
    # def tag_list(self, obj):
    #     return u", ".join(o.name for o in obj.tags.all())

    @models.permalink
    def get_absolute_url(self):
        return 'blog:post', (self.slug,)

    def __str__(self):
         return self.title

class Image(models.Model):
    #owner = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    date_added = models.DateTimeField(auto_now_add=True)

    image = models.FileField(upload_to=get_filename, verbose_name='Images')
    #tags = TaggableManager()

