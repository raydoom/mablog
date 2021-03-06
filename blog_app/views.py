#! /usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm
import markdown
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
import logging

# Create your views here.

logger = logging.getLogger('blog_app')

#def index(request): #index 函数视图
#	post_list = Post.objects.all().order_by('-created_time')
#	return render(request, 'blog/index.html', context={'post_list': post_list})

class IndexView(ListView): #index 类视图
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by = 4
	logger.debug('blog_app log hello')

	def get_queryset(self):
		post_list = Post.objects.all().order_by('-created_time') #按创建时间反向排序

		for post in post_list: #index页面评论数量
			post.comments_counter = post.comment_set.all().count()
		return post_list
		
		logger.debug('blog_app log1 hello')


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		pagination_data = self.pagination_data(paginator, page,is_paginated)
		context.update(pagination_data)
		return context

	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			return {}

		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False
		page_number = page.number
		total_pages = paginator.num_pages
		page_range = paginator.page_range

		if page_number == 1:
			right = page_range[page_number:page_number + 2]
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		data = {
		        'left': left,
		        'right': right,
		        'left_has_more': left_has_more,
		        'right_has_more': right_has_more,
		        'first': first,
		        'last': last,
        		}

		return data



#def archives(request,year,month): #归档函数视图
#	post_list = Post.objects.filter(created_time__year = year,
#									created_time__month = month).order_by('-created_time')
#	return render(request, 'blog/index.html', context={'post_list': post_list})

class ArchivesView(IndexView):
	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesView,self).get_queryset().filter(created_time__year = year,
															  created_time__month = month)

#def category(request,pk): #目录函数视图
#	cate = get_object_or_404(Category, pk=pk)
#	post_list = Post.objects.filter(category = cate).order_by('-created_time')
#	return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(IndexView): #目录类视图
	def get_queryset(self):
#		cate = get_object_or_404(Category,pk = self.kwargs.get('pk')) #方法一
		cate = self.kwargs.get('pk')  #方法二
		return super(CategoryView,self).get_queryset().filter(category = cate)

class TagView(IndexView): #标签类视图
	def get_queryset(self):
		tag = self.kwargs.get('pk')  
		return super(TagView,self).get_queryset().filter(tags = tag)


def detail(request,pk): #文章页面函数视图
	post = get_object_or_404(Post,pk=pk)

	post.increase_views()
	post.body = markdown.markdown(post.body,
		extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.toc',
		])

	form = CommentForm() #comments相关
	comment_list = post.comment_set.all() #comments相关
	print (comment_list)
	context = {'post':post,
				'form':form,
				'comment_list':comment_list
				}

	return render(request,'blog/detail.html',context = context)

class PostDetailView(DetailView): #文章页面类视图
	model = Post
	template_name = 'blog/detail.html'
	context_object_name = 'post'

	def get(self, request, *args, **kwargs):
		response = super(PostDetailView, self).get(request, *args, **kwargs)
		self.object.increase_views()
		return response

	def get_object(self, get_queryset = None):
		post = super(PostDetailView, self).get_object(queryset=None)
		post.body = markdown.markdown(post.body,
										extensions=[
											'markdown.extensions.extra',
											'markdown.extensions.codehilite',
											'markdown.extensions.toc',
										])
		return post

	def get_context_data(self,**kwargs):
		context = super(PostDetailView,self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all().order_by('-created_time') #文章详情页面评论显示
		comment_count = self.object.comment_set.all().count() #文章详情页面评论数量
		context.update({'form':form,
						'comment_list':comment_list,
						'comment_count':comment_count
						})
		return context

def about(request):
	return render(request,'blog/about.html')

def contact(request):
	return render(request,'blog/contact.html')