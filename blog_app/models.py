#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

# Create your models here.

class Category(models.Model): #目录
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Tag(models.Model): #标签
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model): #文章内容
    title = models.CharField(max_length=70)
    body = models.TextField()

    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    excerpt = models.CharField(max_length=200, blank=True) #文章摘要

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    views = models.PositiveIntegerField(default=0)  #阅读量  

    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	return reverse('blog_app:detail',kwargs = {'pk':self.pk})

    def increase_views(self): #更新阅读量函数
        self.views +=1
        self.save(update_fields=['views'])

    #用户 myuser  密码 mxd123456


