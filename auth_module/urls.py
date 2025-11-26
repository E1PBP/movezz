from django.urls import path
from django.http import HttpResponse
from .views import login_view, logout_user, register_view, login_api, register_api, logout_api

app_name = 'auth_module'

urlpatterns = [
    # path('', lambda request: HttpResponse(''), name='empty'),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_view, name='register'),
    path('api/login/', login_api, name='api_login'),
    path('api/register/', register_api, name='api_register'),
    path('api/logout/', logout_api, name='api_logout'),
]

