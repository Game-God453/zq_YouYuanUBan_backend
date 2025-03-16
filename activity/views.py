from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from activity.models import Activity
from user.models import User
import json
from django.core import serializers
from datetime import datetime
from user.tools.userGet import userGet
from user.tools.aliyun_fileupdate import upload_image


# Create your views here.
def activity_list(request):
    raw=Activity.objects.all()
    raw=serializers.serialize('json',raw)
    raw=json.loads(raw)
    data=[]
    for act in raw:
        a=act['fields']
        id=act['pk']
        a['actID']=id
        a['images']=json.loads(a['images'])
        data.append(a)
    a=Activity.objects.all().first()
    author=a.author
    # print(author.openid)
    print(author.activity_author.first().title)
    for obj in author.activity_author.all():
        print(obj.title)
    # print(data)
    return JsonResponse({
        'data':data,
        'message':'查询成功',
        'status':200
    })

# 
def add_activity(request):
    data=json.loads(request.body)
    # print(type(data))
    #处理时间类型
    date_str = data.get('date')
    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(date_str, date_format).date()
    data['date']=date_obj
    
    user=userGet(request)
    data['author']=user
    
    data['images']=json.dumps(data.get('images'))
    
    Activity.objects.create(**data)
    return JsonResponse({
            # 'data':data,
            'message':'添加成功！',
            'status': 200
        })

def del_activity(request):
    data=json.loads(request.body)
    act=Activity.objects.get(actID=data['actID'])
    act.participants.clear()
    act.delete()
    return JsonResponse({
        'message':'删除成功！',
        'status':200
    })
    
def sign_activity(request):
    data=request.POST
    id=data['actID']
    act=Activity.objects.get(actID=id)
    user=userGet(request)
    act.participants.add(user)
    return JsonResponse({
        'message':'报名成功',
        'status':200,
    })
    
def unsign_activity(request):
    data=request.POST
    id=data['actID']
    act=Activity.objects.get(actID=id)
    user=userGet(request)
    act.participants.remove(user)
    return JsonResponse({
        'message':'取消成功',
        'status':200
    })
    
def show_user_activities(request):
    user=userGet(request)
    raw=user.activity_participants.all()
    raw=serializers.serialize('json',raw)
    raw=json.loads(raw)
    data=[]
    for act in raw:
        a=act['fields']
        id=act['pk']
        a['actID']=id
        a['images']=json.loads(a['images'])
        data.append(a)
    return JsonResponse({
        'data':data,
        'message':'查询成功',
        'status':200
    })
    
def fileUpload(request):
    user = userGet(request)
    json_response, url = upload_image(request)
    return json_response