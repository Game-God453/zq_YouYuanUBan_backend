from django.urls import path

from chat_longpolling import views

urlpatterns = [
    path('send',views.send_message,name='send_message'),
    path('get',views.get_messages,name='get_messages'),
]