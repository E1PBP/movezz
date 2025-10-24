from django.urls import path
from django.http import HttpResponse
from . import views



app_name = 'message_module'


urlpatterns = [
    path("", views.chat_view, name="chat_home"),
    path("start/@<str:username>/", views.start_chat, name="start_chat"),
    path("<uuid:conversation_id>/", views.chat_view, name="chat_view"),
    path("<uuid:conversation_id>/send/", views.send_message, name="send_message"),
    path("<uuid:conversation_id>/poll/", views.poll_messages, name="poll_messages"),
    # path("poll", views.start_conversation, name="start_conversation"),
]
