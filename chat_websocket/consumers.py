# import json
# from logging import exception
#
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.exceptions import DenyConnection
#
# from django.contrib.auth import authenticate
# from django_redis import get_redis_connection
#
# from user.models import User
# from user.tools.JWTtoken import JWTToken
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # 获取WebSocket URL中的参数（例如Token）
#         token = self.scope['url_route']['kwargs'].get('token')
#
#         user = await self.authenticate_user(token)
#
#         if user is None:
#             raise DenyConnection("Invalid Token")  # 如果Token无效，拒绝连接
#
#         self.room_name = self.scope['url_route']['kwargs']['userId']
#
#         self.room_group_name = f'chat_{self.room_name}'
#
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         sender = text_data_json['sender']
#         receiver = text_data_json['receiver']
#
#         print(message)
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'sender': sender,
#                 'receiver': receiver,
#                 'message': message,
#             }
#         )
#
#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']
#         receiver = event['receiver']
#
#         # await self.send(text_data=json.dumps({
#         #     'sender': sender,
#         #     'receiver': receiver,
#         #     'message': message,
#         # }))
#
#         await self.send(text_data=message)
#
#     @database_sync_to_async
#     def authenticate_user(self, token):
#         # 在这里实现你的Token验证逻辑
#         payload,message = JWTToken.decode(token=token)
#         if not payload:
#             return None
#
#         redis_conn = get_redis_connection("default")
#         stored_token = redis_conn.get(f"token:{payload['openid']}")
#         if not stored_token or stored_token.decode('utf-8') != token:
#             return None
#
#         openid = payload.get('openid')
#         user = User.objects.filter(openid=openid).first()
#         return user