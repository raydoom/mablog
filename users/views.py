from django.shortcuts import render, redirect
from .forms import RegisterForm
import logging

# Create your views here.
logger = logging.getLogger('users')

def register(request):
	logger.debug('users log hello')
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			logger.debug(form)
			return redirect('/users/login/?next=/')

	else:
		form = RegisterForm()

	return render(request,'users/register.html',context={'form':form})

def index(request):
	return render(request,'index.html')
