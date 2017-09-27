# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Post, Category, Tag
from users.models import Users

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

class UsersAdmin(admin.ModelAdmin):
	list_display = ['username', 'nikename', 'email','last_login']

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Users,UsersAdmin)


# admin mxd111111

