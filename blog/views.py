from django.shortcuts import render
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
#from django.contrib.auth.decorators import login_required


from .forms import *

# --------------- Main Views ---------------

def index(request):
	"""Project logs home page"""
	return render(request, 'blog/index.html')

#TODO: def table_of_contents():
#TODO: def post_detail():

# --------------- Post Views ---------------

#TODO: rename to add_post
def post(request):
	ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)

	if request.method != 'POST':
		postform = PostForm()
		formset = ImageFormSet(queryset=Image.objects.none())

	else:
		postform = PostForm(request.POST)
		formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

		if postform.is_valid() and formset.is_valid():
			photo = formset.save()
			data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
			post_form = postform.save(commit=False)
			post_form.user = request.user
			post_form.save()

			for form in formset.cleaned_data:
				image = form['image']
				photo = Image(post=post_form, image=image)
				photo.save()
			return HttpResponseRedirect(reverse('blog:index'))

	context = {'postForm': postform, 'formset': formset}
	return render(request, 'blog/post.html', context)

#TODO: def edit_post():

# --------------- Image Views ---------------

def add_images(request, post_id, num):
	ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=num)
	post = Post.objects.get(id=post_id)

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
				return HttpResponseRedirect('blog:index', args=[post_id])

	context = {'post': post, 'formset': formset}
	return render(request, 'blog/post.html', context)

#TODO: def remove_images():
