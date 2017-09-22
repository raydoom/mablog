#blog_app urls

from django.conf.urls import url
from . import views

app_name = 'blog_app'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
	url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
]
