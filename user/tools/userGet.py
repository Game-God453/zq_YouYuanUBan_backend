from django.http import JsonResponse

from user.models import User
from user.tools.JWTtoken import JWTToken


def userGet(request):
    token = request.headers.get('Authorization')
    payload = JWTToken.decode(token)
    openid = payload.get('openid')
    user = User.objects.filter(openid=openid).first()
    if not user:
        return None
    return user

def userNotExist():
    return JsonResponse({
        'data': None,
        'message': "当前用户不存在！",
        'status': 400})
