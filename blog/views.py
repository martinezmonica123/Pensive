from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import View

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse

#from django.contrib.auth.decorators import login_required

from .forms import *


# --------------- Main Views ---------------
def index(request):
	"""Project logs home page --- currently redirects to all content view"""
	return HttpResponseRedirect(reverse('blog:contents'))

def contents(request):
	posts = Post.objects.all().order_by('-date_added')
	images = Image.objects.all().order_by('-date_added')
	context = {'posts': posts, 'images': images}
	return render(request, 'blog/all_posts.html', context)


# --------------- Image Views ---------------
#TODO: def remove_images():


class ImageView(View):
	def get(self, request, slug):
		print('here')
		post = get_object_or_404(Post, slug=slug)
		images = post.image_set.order_by('-date_added')

		context = {'post': post, 'images': images}
		return render(self.request, 'blog/add_images.html', context)

	def post(self, request, slug):
		# ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)
		# post = get_object_or_404(Post, slug=slug)
        #
		# if request.method != 'POST':
		# 	formset = ImageFormSet(queryset=Image.objects.none())
		# else:
		# 	formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
		# 	if formset.is_valid():
		# 		for form in formset.cleaned_data:
		# 			image = form['image']
		# 			photo = Image(image=image)
		# 			photo.post = post
		# 			photo.save()
		# 			return HttpResponseRedirect(reverse('blog:post', args=[slug]))
        #
		# context = {'post': post, 'formset': formset}
		# return render(request, 'blog/add_images.html', context)
		#
		form = ImageForm(self.request.POST, self.request.FILES)
		post = get_object_or_404(Post, slug=slug)

		if form.is_valid():
			print('made it here 2')
			image = form.cleaned_data['image']
			photo = Image(image=image)
			photo.post = post
			photo.save()
			data = {'is_valid': True, 'name': photo.image.name, 'url': photo.image.url}

		else:
			print('made it here 3')
			data = {'is_valid': False}
		return JsonResponse(data)


# --------------- Post Views ---------------
#TODO: def edit_post():


def post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	images = post.image_set.order_by('-date_added')

	#if project.owner != request.user:
	#	raise Http404

	context = {'post': post, 'images': images}
	return render(request, 'blog/post_detail.html', context)


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

