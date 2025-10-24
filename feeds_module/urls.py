from django.urls import path
from feeds_module.views import main_view, create_post_ajax, load_more_posts, like_post_ajax

app_name = 'feeds_module'

urlpatterns = [
    path('', main_view, name='main_view'),
    path('create_post/', create_post_ajax, name='create_post_ajax'),
    path('load_more/', load_more_posts, name='load_more_posts'),
    path('like_post/', like_post_ajax, name='like_post_ajax'),
]

