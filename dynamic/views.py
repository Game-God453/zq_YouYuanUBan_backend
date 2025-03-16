from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from activity.models import Activity
from user.models import User
from dynamic.models import Dynamic,Comment
import json
from django.core import serializers
from datetime import datetime
from user.tools.userGet import userGet
from user.tools.aliyun_fileupdate import upload_image
# Create your views here.

def add_dynamic(request):
    data=json.loads(request.body)
    
    user=userGet(request)
    data['author']=user
    data['images']=json.dumps(data.get('images'))
    
    Dynamic.objects.create(**data)
    
    return JsonResponse({
        'message':'发布成功',
        'status':200
    })
    
def del_dynamic(request):
    data=json.loads(request.body)
    id=data['id']
    Dynamic.objects.get(id=id).delete()
    return JsonResponse({
        'message':'删除成功',
        'status':200
    })
    
def user_dynamic(request):
    user=userGet(request)
    raw=user.dynamic_author.all()
    raw=serializers.serialize('json',raw)
    raw=json.loads(raw)
    data=[]
    for dyn in raw:
        a=dyn['fields']
        id=dyn['pk']
        a['dynID']=id
        a['images']=json.loads(a['images'])
        data.append(a)
    return JsonResponse({
        'data':data,
        'message':'查询成功',
        'status':200
    })
    
    
def add_comment(request):
    data=json.loads(request.body)
    user=userGet(request)
    dyn=Dynamic.objects.get(id=data['dynID'])
    Comment.objects.create(author=user,dynamic=dyn,comment=data['comment'])
    return JsonResponse({
        'message':'发布成功',
        'status':200
    })
    
def del_comment(request):
    data=json.loads(request.body)
    id=data['id']
    Comment.objects.get(id=id).delete()
    return JsonResponse({
        'message':'删除成功',
        'status':200
    })
    
def show_comments(request):
    data=json.loads(request.body)
    dyn=Dynamic.objects.get(id=data['dynID'])
    raw=dyn.comment_dynamic.all()
    raw=serializers.serialize('json',raw)
    raw=json.loads(raw)
    data=[]
    for com in raw:
        a=com['fields']
        id=com['pk']
        a['id']=id
        data.append(a)
    return JsonResponse({
        'data':data,
        'message':'查询成功',
        'status':200
    })