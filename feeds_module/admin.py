from django.contrib import admin
from .models import Post, PostImage, PostLike, Comment, CommentLike, PostHashtag
# Register your models here.

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(PostHashtag)
