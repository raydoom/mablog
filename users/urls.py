from django.conf.urls import url

from .import views

app_name = 'users'

urlpatterns = [
				 url(r'^register/', views.register, name='register'),
				 url(r'^userinfo/', views.userinfo, name='userinfo'),
				 #url(r'^password_change/', views.password_change, name='password_change'),
			]