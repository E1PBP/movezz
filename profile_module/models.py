from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=80, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(blank=True) # mungkin nanti ini bisa diubah lagi
    cover = models.ImageField(blank=True) # mungkin nanti ini bisa diubah lagi
    current_status = models.CharField(max_length=120, blank=True)
    current_sport_id = models.ForeignKey('Sports', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    stats_posts = models.IntegerField(default=0)
    stats_duration_min = models.IntegerField(default=0)
    stats_distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    followers_count = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Sports(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=80)
    icon_url = models.ImageField(blank=True) # mungkin nanti ini bisa diubah lagi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'sports'
        verbose_name = 'Sport'
        verbose_name_plural = 'Sports'
        
class UserSports(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    sport_id = models.ForeignKey(Sports, on_delete=models.CASCADE)
    profiency_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.user_id.username} - {self.sport_id.name}"


class Follows(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        db_table = 'follows'
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    
class Badges(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.ImageField(blank=True) # mungkin nanti ini bisa diubah lagi
    
class UserBadge(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_id = models.ForeignKey(Badges, on_delete=models.CASCADE)