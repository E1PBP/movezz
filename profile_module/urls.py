from django.urls import path, include
from django.http import HttpResponse
from . import views

app_name = 'profile_module'

urlpatterns = [
    path("", views.profile_detail, name="profile_home"),
    path("u/<str:username>/", views.profile_detail, name="profile_detail"),
    path("u/<str:username>/p/<slug:pk>/", views.post_detail, name="post_detail"),
    path("@<str:username>/", views.profile_detail, name="profile_detail"),
    path("@<str:username>/follow/", views.follow_user, name="follow"),
    path("@<str:username>/unfollow/", views.unfollow_user, name="unfollow"),
    path("api/follow/<str:username>/toggle/", views.follow_toggle_ajax, name="follow_toggle"),
    path("api/posts/<slug:pk>/update/", views.post_update_ajax, name="post_update"),
    path("api/posts/<slug:pk>/delete/", views.post_delete_ajax, name="post_delete"),
    path("api/broadcasts/create/", views.create_broadcast_ajax, name="create_broadcast_ajax"),
    path("api/u/<str:username>/", views.profile_detail_api, name="profile_detail_api"),
    path("api/u/<str:username>/posts/", views.user_posts_api, name="user_posts_api"),
    # path("broadcast/<uuid:pk>/toggle-pin/", views.toggle_broadcast_pin, name="toggle_broadcast_pin"),
]