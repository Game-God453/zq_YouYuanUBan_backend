from django.urls import path
from dynamic import views

urlpatterns = [
    path('add',views.add_dynamic),
    path('del',views.del_dynamic),
    path('comment/add',views.add_comment),
    path('comment/del',views.del_comment),
    path('showDynamics',views.user_dynamic),
    path('showComments',views.show_comments)
]
