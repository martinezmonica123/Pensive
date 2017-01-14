from django.shortcuts import render
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Post, Images
from .forms import PostForm, ImageForm
# Create your views here.

def index(request):
	"""Project logs home page"""
	return render(request, 'blog/index.html')

def post(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)

    if request.method != 'POST':
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    else:
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(post=post_form, image=image)
                photo.save()
            #messages.success(request,"Yeeew,check it out on the home page!")
            return HttpResponseRedirect(reverse('blog:index'))

    context = {'postForm': postForm, 'formset': formset}
    return render(request, 'blog/post.html', context)