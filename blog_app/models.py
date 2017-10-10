#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown

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

    title = models.CharField(max_length=25)
    body = models.TextField()

    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    excerpt = models.CharField(max_length=200, blank=True) #文章摘要

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    views = models.PositiveIntegerField(default=0)  #阅读量  

    comments_counter = '0'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	return reverse('blog_app:detail',kwargs = {'pk':self.pk})

    def increase_views(self): #更新阅读量函数
        self.views +=1
        self.save(update_fields=['views'])

    def save(self,*args,**kwargs): #自动生成摘要
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ])
            self.excerpt = md.convert(self.body)[:108]+'......'
        super(Post, self).save(*args, **kwargs)
   

    #用户 myuser  密码 mxd123456


