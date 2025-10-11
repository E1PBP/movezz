from django.urls import path
from django.http import HttpResponse

app_name = 'profile_module'

urlpatterns = [
    path('', lambda request: HttpResponse(''), name='empty'),
]

