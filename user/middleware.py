# users/middleware.py
from django.http import JsonResponse
from django.urls import reverse
from django_redis import get_redis_connection

from user.models import User
from user.tools.JWTtoken import JWTToken


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        #如果是登录，则直接处理请求
        if request.path.startswith(reverse('login')):
            return self.get_response(request)

        # 检查用户是否已经登录
        token = request.headers.get('Authorization')
        payload, error_message = JWTToken.decode(token=token)

        if not payload:
            # 返回 JSON 格式的提示信息
            return JsonResponse({
                "data": None,
                "message": error_message,
                "status": 401  # 401 表示未授权
            })

        openid = payload.get('openid')
        user = User.objects.filter(openid=openid).exists()
        if not user:
            return JsonResponse({
                "data": None,
                "message": "当前用户未注册或已注销",
                "status": 404
            })

        redis_conn = get_redis_connection("default")
        stored_token = redis_conn.get(f"token:{payload['openid']}")

        if not stored_token or stored_token.decode('utf-8')!= token:
            return JsonResponse({
                "data": None,
                "message": "超过认证时间，请重新登录",
                "status": 401  # 401 表示未授权
            })

        return self.get_response(request)

