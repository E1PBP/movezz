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
]
