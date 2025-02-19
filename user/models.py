from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 添加自定义字段
    openid = models.CharField(verbose_name='openid', max_length=64,unique=True,default="未获取openid")
    avatar = models.URLField(null=True, blank=True)
    birthday = models.DateField(null=True)
    password = models.CharField(verbose_name='password',max_length=64,null=True,blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(verbose_name='username',max_length=15,validators=[validators.MinLengthValidator(1)],unique=True,null=True,blank=True)
    email = models.EmailField(verbose_name='email',max_length=64,unique=True,null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'openid'

    class Meta:
        db_table = 'our_user'





