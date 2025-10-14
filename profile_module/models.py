from django.conf import settings
from django.db import models
from django.utils import timezone
from common.models import Sport, Badge
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=80, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    current_sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    post_count = models.BigIntegerField(default=0)
    broadcast_count = models.BigIntegerField(default=0)
    following_count = models.BigIntegerField(default=0)
    followers_count = models.BigIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.display_name or str(self.user)

class UserSport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    time_elapsed = models.DurationField(default='0')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "sport")

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follows_given", on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name="follows_received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("follower", "followee")

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "badge")
