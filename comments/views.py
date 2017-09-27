from django.shortcuts import render, get_object_or_404, redirect
from blog_app.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here. comment

def post_comment(request,post_pk):
	post = get_object_or_404(Post,pk=post_pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		print (request.user.username)

		if form.is_valid():
			comment = form.save(commit=False)
			comment.name = request.user.nikename #设定评论用户为当前登陆
			comment.post = post
			comment.save()
			return redirect(post)

		else:
			comment_list = post.comment_set.all()
			context = {'post':post,
						'form':form,
						'comment_list':comment_list,
						'comment_count':comment_count,
						}
			return render(request,'blog_app/detail.html',context=context)

	return redirect(post)

