from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import AutoField, BooleanField, EmailField
# Create your models here.

class User(AbstractUser):
    username = models.CharField(  # username是必需有的字段，字段名不能错
        max_length=20,
        null=False,
        blank=False,
        verbose_name='用户名'
    )
    password = models.CharField(max_length=256,null = False,blank=False,verbose_name="密码")
    plce = models.CharField(max_length=32,null=False,blank=False,verbose_name="地区")
    email = EmailField(unique=True)  # 给email弄成唯一的
    USERNAME_FIELD = 'email'  # 默认是username，这个字段有唯一索引
    REQUIRED_FIELDS = ['username']  # 指定必填字段，这里不填userna