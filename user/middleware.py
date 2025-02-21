# users/middleware.py
from django.http import JsonResponse
from django.urls import reverse
from django_redis import get_redis_connection

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
        payload = JWTToken.decode(token=token)

        if not payload:
            # 返回 JSON 格式的提示信息
            return JsonResponse({
                "data": None,
                "message": "未登录，请先登录！",
                "status": 401  # 401 表示未授权
            })
        redis_conn = get_redis_connection("default")
        stored_token = redis_conn.get(f"token:{payload['openid']}").decode('utf-8')

        if stored_token != token:
            return JsonResponse({
                "data": None,
                "message": "当前登录已失效，请重新登录",
                "status": 401  # 401 表示未授权
            })

        return self.get_response(request)

