from django.db import models
from django.db.models import F, Max
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user.tools.userGet import userGet
from .models import ChatConnection, Message
import time

# 发送消息
@csrf_exempt
def send_message(request):
    if request.method == "POST":

        sender = userGet(request)

        receiver_id = request.POST.get("receiver_id")
        receiver = User.objects.filter(id=receiver_id).first()
        if not receiver:
            return JsonResponse({
                'data': None,
                'message': '发送的消息对象不存在！',
                'status': 400
            })

        content = request.POST.get("content")

        connection = ChatConnection.objects.filter(
                models.Q(user1=sender) & models.Q(user2=receiver)
                | models.Q(user1=receiver) & models.Q(user2=sender)
            ).first()

        message = Message.objects.create(
            chat=connection,
            sender=sender,
            receiver=receiver,
            content=content
        )

        return JsonResponse({
                'data': None,
                'message': '消息发送成功',
                'status': 200
            })

    return JsonResponse({
                'data': None,
                'message': '无效请求，消息发送失败',
                'status': 400
            })

# 长轮询获取消息
@csrf_exempt
def get_messages(request):
    if request.method == "GET":
        user = userGet(request)
        timeout = 20  # 设置超时时间（秒）
        start_time = time.time()

        while True:
            # 查询所有与该用户相关的聊天连接
            connections = ChatConnection.objects.filter(
                models.Q(user1=user) | models.Q(user2=user)
            )

            # 查询所有新消息
            new_messages = []
            for connection in connections:
                if connection.user1 == user:
                    last_message_id = connection.last_message_user1
                else:
                    last_message_id = connection.last_message_user2

                # 获取当前连接中，消息 ID 大于 last_message_id 的消息
                messages = connection.messages.filter(id__gt=last_message_id).order_by('timestamp')
                new_messages.extend(messages)

                #记录聊天的最新消息id
                if messages.exists():
                    if connection.user1 == user:
                        connection.last_message_user1 = messages.aggregate(Max('id'))['id__max']
                        connection.save()
                    else:
                        connection.last_message_user2 = messages.aggregate(Max('id'))['id__max']
                        connection.save()


            if new_messages:
                # 按发送方分组消息
                grouped_messages = {}
                for msg in new_messages:
                    sender_id = msg.sender.id
                    if sender_id not in grouped_messages:
                        grouped_messages[sender_id] = []
                    grouped_messages[sender_id].append({
                        "isSelf": msg.receiver.id if sender_id == user.id else False,
                        "content": msg.content,
                        "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    })
                return JsonResponse({
                    'data': grouped_messages,
                    'message': '成功获取新消息',
                    'status': 200
                })

            # 检查是否超时
            if time.time() - start_time > timeout:
                return JsonResponse({
                    'data': {},
                    'message': '无新消息',
                    'status': 200
                })

            # 短暂休眠，避免CPU占用过高
            time.sleep(1)

    return JsonResponse({
                'data': None,
                'message': '无效请求，消息发送失败',
                'status': 400
            })