from django.urls import path

from friends import views

urlpatterns = [
    path('send_friend_request/<int:to_user_id>', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>', views.accept_friend_request, name='accept_friend_request'),
    path('delete_friend/<int:friend_id>', views.delete_friend, name='delete_friend'),
    path('get_request_list', views.get_request_list, name='get_request_list'),
    path('get_friend_list', views.get_friend_list, name='get_friend_list'),
]