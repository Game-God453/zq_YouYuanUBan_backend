from django.db import models

# Create your models here.
class Activity(models.Model):
    # actID=models.AutoField()# 活动 ID
    title=models.CharField(max_length=32)
    price=models.CharField(max_length=32)
    address=models.CharField(max_length=32)
    detailAddress=models.CharField(max_length=32)
    date=models.DateField(default='2005-05-20')
    time=models.CharField(max_length=32)
    status=models.CharField(max_length=32)#包括正在报名，报名结束，已报名（根据用户ID查询）
    # participants=models.IntegerField()
    plan=models.IntegerField()
    tag=models.CharField(max_length=32)
    description=models.CharField(max_length=64)
    authorID=models.CharField(max_length=32) #昵称
    authorAvatar=models.CharField(max_length=32) #头像
    
