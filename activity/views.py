from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from activity.models import Activity


from datetime import datetime

# Create your views here.
def activity_list(request):
    return HttpResponse('活动列表')

# 
def add_activity(request):
    # print(request)
    data=request.POST.dict()
    print(data)
    date_str = data.get('date')
    print(date_str)
    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(date_str, date_format).date()
    print(date_obj) # 输出: 2022-01-01
    data['date']=date_obj
    Activity.objects.create(**data)
    return HttpResponse('添加成功')