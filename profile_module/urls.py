from django.urls import path, include
from django.http import HttpResponse
from . import views

app_name = 'profile_module'

urlpatterns = [
    path(" ", views.profile_detail, name="profile_home"),
    path("@<str:username>", views.profile_detail, name="profile_detail"),
    path("@<str:username>/follow/", views.follow_user, name="follow"),
    path("@<str:username>/unfollow/", views.unfollow_user, name="unfollow"),
]

