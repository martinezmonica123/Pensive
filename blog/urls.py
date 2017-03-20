"""Defines URL patterns for Project_logs"""

from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^$', views.index, name='index'),
    url(r'^all-posts/$', views.contents, name='contents'),
    url(r'^post/(?P<slug>[-\w]+)/$', views.post, name='post'),
    url(r'^new-post/$', views.new_post, name='new_post'),
    url(r'^add-images/(?P<slug>[-\w]+)/$', views.add_images, name='add_images'),
]