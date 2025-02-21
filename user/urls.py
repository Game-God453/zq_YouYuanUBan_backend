from django.urls import path

from user import views

urlpatterns = [
    path("login",views.user_login,name="login"),
    path("info",views.user_info,name="user_info"),
    path("update",views.user_update,name="user_update"),
    path("fileUpload",views.user_fileUpload,name="user_fileUpload"),

]