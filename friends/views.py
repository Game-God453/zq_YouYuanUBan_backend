from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from user.tools.userGet import userGet, userNotExist
from .models import FriendRequest, Friendship
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()  # 获取自定义用户模型

@require_http_methods(['POST'])
def send_friend_request(request, to_user_id):
    try:
        to_user = get_object_or_404(User, id=to_user_id)
    except Http404:
        return JsonResponse({
            'data': None,
            'message': '对方不存在',
            'status': 404
        })
    from_user = userGet(request)

    if from_user != to_user:
        exist1 = Friendship.objects.filter(user1=to_user, user2=from_user).exists()
        exist2 = Friendship.objects.filter(user1=from_user, user2=to_user).exists()
        #如果好友关系已经建立，无需发送申请
        if exist1 or exist2:
            return JsonResponse({
                'data': None,
                'message': '对方已是你的好友',
                'status': 200
            })
        fr, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        #如果已经发送过申请
        if not created:
            #如果申请未被接受，则不能重复发送
            if not fr.accepted:
                return JsonResponse({
                    'data': None,
                    'message': '好友请求已发送，不要重复发送',
                    'status': 200
                })
            #如果申请被接受，说明二者好友关系被删除，则可以重新发送好友申请
            else:
                FriendRequest.objects.create(from_user=from_user, to_user=to_user)

        return JsonResponse({
            'data': fr.id,
            'message': '好友请求发送成功',
            'status': 200
        })
    return JsonResponse({
        'data': None,
        'message': '好友请求发送失败',
        'status': 200
    })

@require_http_methods(['POST'])
def accept_friend_request(request, request_id):
    try:
        friend_request = get_object_or_404(FriendRequest, id=request_id)
    except Http404:
        return JsonResponse({
            'data': None,
            'message': '此好友请求不存在',
            'status': 404
        })

    request_user = userGet(request)
    if friend_request.to_user == request_user:
        # 如果对方已经添加请求用户为好友则无需接受（说明用户也像对方发送过好友请求并已被接受）
        exist = Friendship.objects.filter(user1=friend_request.to_user, user2=friend_request.from_user).exists()
        if exist:
            return JsonResponse({
                'data': None,
                'message': '对方已添加你为好友',
                'status': 200
            })
        #如果用户已经添加对方好友则无需重复接受
        fs1,created1 = Friendship.objects.get_or_create(user1=friend_request.from_user, user2=friend_request.to_user)
        if not created1:
            return JsonResponse({
                'data': None,
                'message': '对方已是你的好友，请勿重复接受',
                'status': 200
            })
        #设置好友申请单的状态为已同意
        friend_request.accepted = True
        friend_request.save()
        return JsonResponse({
            'data': None,
            'message': '好友请求接受成功',
            'status': 200
        })
    return JsonResponse({
        'data': None,
        'message': '好友申请的对象与当前用户不匹配！',
        'status': 200
    })

@require_http_methods(['POST'])
def delete_friend(request, friend_id):
    try:
        friend = get_object_or_404(User, id=friend_id)
    except Http404:
        return JsonResponse({
            'data': None,
            'message': '该用户不存在',
            'status': 404
        })
    request_user = userGet(request)

    if friend == request_user:
        return JsonResponse({
            'data': None,
            'message': '无效操作，不能删除自己',
            'status': 200
        })

    fs1 = Friendship.objects.filter(user1=request_user, user2=friend).first()
    fs2 = Friendship.objects.filter(user1=friend, user2=request_user).first()
    if not fs1 and not fs2:
        return JsonResponse({
            'data': None,
            'message': '好友已删除或对方不是你的好友',
            'status': 200
        })
    if fs1:
        fs1.delete()
    if fs2:
        fs2.delete()
    return JsonResponse({
    'data': None,
    'message': '好友删除成功',
    'status': 200
    })

@require_http_methods(['GET'])
def get_request_list(request):
    user = userGet(request)
    request_list = []
    for friendrequest in FriendRequest.objects.filter(to_user=user):
        request_list.append({'userId': friendrequest.from_user.id, 'username': friendrequest.from_user.username, 'status': friendrequest.accepted})
    return JsonResponse({
        'data': request_list,
        'message': '获取好友请求列表成功',
        'status': 200
    })

@require_http_methods(['GET'])
def get_friend_list(request):
    user = userGet(request)
    friends = []
    for friendship in Friendship.objects.filter(user1=user):
        friends.append({'userId': friendship.user2.id, 'username': friendship.user2.username})
    for friendship in Friendship.objects.filter(user2=user):
        friends.append({'userId': friendship.user1.id, 'username': friendship.user1.username})
    return JsonResponse({'friends': friends})