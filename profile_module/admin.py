from django.contrib import admin
from .models import Profile, UserSport, Follow, UserBadge
# Register your models here.
admin.site.register(Profile)
admin.site.register(UserSport)
admin.site.register(Follow)
admin.site.register(UserBadge)