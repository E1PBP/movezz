from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views

app_name = 'broadcast_module'

urlpatterns = [
    
    path('', views.broadcast_list, name='list'),
    path('trending/', views.get_trending_events, name='trending'),
    path('latest/', views.get_latest_events, name='latest'),
    
    path('events/<uuid:pk>/click/', views.click_event, name='click'),
    path('events/create/', views.create_event, name='create'),
    
    path('pin/<uuid:pk>/', staff_member_required(views.pin_event), name='pin'),
    path('unpin/<uuid:pk>/', staff_member_required(views.unpin_event), name='unpin'),

    path('api/trending/', views.api_trending_events, name='api_trending'),
    path('api/latest/', views.api_latest_events, name='api_latest'),
    path('api/events/create/', views.api_create_event, name='api_create_event'),
    path("api/u/<str:username>/broadcasts/", views.api_user_broadcasts, name="api_user_broadcasts",
),
]
