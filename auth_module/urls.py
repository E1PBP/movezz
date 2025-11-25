from django.urls import path
from django.http import HttpResponse
from .views import login_view, logout_user, register_view, login, register, logout

app_name = 'auth_module'

urlpatterns = [
    # path('', lambda request: HttpResponse(''), name='empty'),
    path('login/', login_view, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_view, name='register'),
    path('api/login/', login, name='api_login'),
    path('api/register/', register, name='api_register'),
    path('api/logout/', logout, name='api_logout'),
]

