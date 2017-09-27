# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
	nikename = models.CharField("昵称",max_length=50,blank=True)
