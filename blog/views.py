from django.shortcuts import get_object_or_404, render
from django.forms import modelformset_factory
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpResponseRedirect
#from django.contrib.auth.decorators import login_required

from .forms import *


# --------------- Main Views ---------------
#TODO: def table_of_contents():
#TODO: def post_detail():

def index(request):
	"""Project logs home page"""
	return render(request, 'blog/index.html')


# --------------- Post Views ---------------
#TODO: def edit_post():

def post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	images = post.image_set.order_by('-date_added')

	#if project.owner != request.user:
	#	raise Http404

	context = {'post': post, 'images': images}
	return render(request, 'blog/post.html', context)


def new_post(request):

	if request.method != 'POST':
		postform = PostForm()

	else:
		postform = PostForm(request.POST)

		if postform.is_valid():
			post_form = postform.save()
			post_form.user = request.user
			post_form.save()
			return HttpResponseRedirect(reverse('blog:post', args=[post_form.slug]))

	context = {'postForm': postform}
	return render(request, 'blog/new_post.html', context)


# --------------- Image Views ---------------
#TODO: def remove_images():

def add_images(request, slug):
	ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)
	post = get_object_or_404(Post, slug=slug)

	if request.method != 'POST':
		formset = ImageFormSet(queryset=Image.objects.none())
	else:
		formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
		if formset.is_valid():
			for form in formset.cleaned_data:
				image = form['image']
				photo = Image(image=image)
				photo.post = post
				photo.save()
				return HttpResponseRedirect(reverse('blog:post', args=[slug]))

	context = {'post': post, 'formset': formset}
	return render(request, 'blog/add_images.html', context)