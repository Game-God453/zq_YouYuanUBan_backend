from django.db import models
from user.models import User

# Create your models here.
class Dynamic(models.Model):
    title=models.CharField(max_length=32)
    content=models.TextField()
    images=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='dynamic_author',null=True,default=None)
    
    
class Comment(models.Model):
    dynamic=models.ForeignKey(Dynamic,on_delete=models.CASCADE,related_name='comment_dynamic',null=True,default=None)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_author',null=True,default=None)
    comment=models.TextField()