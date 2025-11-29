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
    
    # mobile endpoints
    path("api/conversations/", views.get_conversations_api, name="api_conversations"),
    path("api/conversations/<uuid:conversation_id>/messages/", views.get_messages_api, name="api_messages"),
    path("api/start/<str:username>/", views.start_chat_api, name="api_start_chat"),
    path("api/conversations/<uuid:conversation_id>/send/", views.send_message, name="api_send_message"),
    path("api/conversations/<uuid:conversation_id>/poll/", views.poll_messages, name="api_poll_messages"),
    path("api/users/search/", views.search_users_api, name="api_search_users"),
]
