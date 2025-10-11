from django.urls import path
from feeds_module.views import main_view

app_name = 'feeds_module'

urlpatterns = [
    path('', main_view, name='main_view'),
]

