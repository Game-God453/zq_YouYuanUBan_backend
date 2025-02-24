from django.urls import path

from activity import views

urlpatterns = [
    path("list",views.activity_list),
    path("add",views.add_activity),
    path("del",views.del_activity),
    path("sign",views.sign_activity),
    path("showActivities",views.show_user_activities)
]