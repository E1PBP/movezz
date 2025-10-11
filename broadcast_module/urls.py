from django.urls import path
from django.http import HttpResponse

app_name = 'broadcast_module'

urlpatterns = [
    path('', lambda request: HttpResponse(''), name='empty'),
]

