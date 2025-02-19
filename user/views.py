import datetime
import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django_redis import get_redis_connection
from user.models import User
from user.tools.JWTtoken import JWTToken
from user.tools.aliyun_fileupdate import upload_image
from user.tools.userGet import userGet

def userNotExist():
    return JsonResponse({
        'data': None,
        'message': "用户不存在！",
        'status': 400})

##########################################################仅供测试###################################################
import random
import string

def generate_random_string(length=6):
    # 定义字符池，包含大小写字母和数字
    characters = string.ascii_letters + string.digits
    # 使用random.choices随机选择字符
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

#####################################################################################################################


@require_http_methods(['POST'])
def user_login(request):

    code = request.POST.get('code')
    if not code:
        return userNotExist()

    # openid,session_key = Wxlogin.get(code)  #有真实小程序信息方可使用
    openid = generate_random_string()
    # openid = "xxxxxx"
    session_key = generate_random_string(12)

    if openid and session_key:

        user, created = User.objects.get_or_create(openid=openid)
        #连接redis
        redis_conn = get_redis_connection("default")

        #如果当前用户已处于登录状态，则删除之前的token，重新登录
        stored_token = redis_conn.get(f"token:{openid}")
        if stored_token:
            #记录上一次登录的时间
            payload = JWTToken.decode(token=stored_token)
            user.last_login = payload.get("login_time")
            user.save()
            #删除先前的token
            redis_conn.delete(f"token:{openid}")


        token = JWTToken(openid,session_key).encode()
        # 获取缓存时间
        cache_ttl = getattr(settings, "CACHE_TTL", 60)  # 默认值为 1 分钟
        # 设置缓存
        redis_conn.set(f"token:{openid}", token, ex=cache_ttl)

        return JsonResponse({
            'data':token,
            'message':'登陆成功！',
            'status': 200
        })

@require_http_methods(['GET'])
def user_info(request):
    user = userGet(request)
    if not user:
        return userNotExist()

    data = {
        "avatar": user.avatar,
        "nickname": user.username,
        "userID": user.id,
        "birthday": user.birthday,
    }
    return JsonResponse({
        'data': data,
        'message': '用户信息获取成功',
        'status': 200
    })

@require_http_methods(['PUT'])
def user_update(request):
    user = userGet(request)
    if not user:
        return userNotExist()

    try:

        # 解析 request.body 中的 JSON 数据
        data = json.loads(request.body)
        user.username = data['username']
        user.birthday = data['birthday']
        user.save()
        return JsonResponse({
            'data': None,
            'message': '用户信息更新成功',
            'status': 200
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'data': None,
            'message': '用户信息更新失败，注意是否是json格式数据!',
            'status': 400
        })

@require_http_methods(['POST'])
def user_fileUpload(request):
    user = userGet(request)
    if not user:
        return userNotExist()

    return upload_image(request)



