from django.urls import path
from django.http import HttpResponse

app_name = 'message_module'

urlpatterns = [
    path('', lambda request: HttpResponse(''), name='empty'),
]

