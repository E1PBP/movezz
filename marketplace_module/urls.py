from django.urls import path
from django.http import HttpResponse

app_name = 'marketplace_module'

urlpatterns = [
    path('', lambda request: HttpResponse(''), name='empty'),
]

