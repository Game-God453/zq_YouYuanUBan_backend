from django.db import models
from user.models import User

# Create your models here.
class Activity(models.Model):
    actID=models.AutoField(primary_key=True)# 活动 ID
    title=models.CharField(max_length=32)
    price=models.CharField(max_length=32)
    address=models.CharField(max_length=32)
    detailAddress=models.CharField(max_length=32)
    date=models.DateField(default='2005-05-20')
    time=models.CharField(max_length=32)
    status=models.CharField(max_length=32)#包括正在报名，报名结束，已报名（根据用户ID查询）
    participants=models.ManyToManyField(User,related_name='activity_participants',default=None)
    plan=models.IntegerField()
    tag=models.CharField(max_length=32)
    description=models.CharField(max_length=64)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='activity_author',null=True,default=None)
    
