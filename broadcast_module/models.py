import uuid
from django.db import models
from django.utils import timezone
from common.models import Sport
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_display_name = models.CharField(max_length=80, blank=True, null=True)
    author_avatar_url = models.TextField(blank=True, null=True)
    author_badges_url = models.TextField(blank=True, null=True)
    community_id = models.UUIDField(null=True, blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    location_name = models.CharField(max_length=120, blank=True, null=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    fee = models.BigIntegerField(null=True, blank=True)
    total_click = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "event")

class EventImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField("image", validators=[validate_image_size], null=True, blank=True)
