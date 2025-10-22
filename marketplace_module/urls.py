from django.urls import path
from django.http import HttpResponse
from . import views

app_name = 'marketplace_module'

urlpatterns = [
    path('', views.todays_pick, name='todays_pick'),
    path('todays-pick/', views.todays_pick, name='todays_pick'),
    path('listing/<uuid:pk>/', views.listing_detail, name='listing_detail'),
    ]

