from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from activity.models import Activity

# Create your views here.
def activity_list(request):
    return HttpResponse('活动列表')

# 
def add_activity(request):
    # data=request.POST
    # Activity.objects.create(**data)
    return HttpResponse('添加成功')