import uuid
from django.db import models
from django.utils import timezone
from common.models import Sport
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size
from django.db.models import Q

class Event(models.Model):
    """
    Represents an event in the broadcast module.
    Fields:
        id (UUIDField): Unique identifier for the event.
        user (OneToOneField): The user who created the event.
        author_display_name (CharField): Display name of the event author.
        author_avatar_url (TextField): URL to the author's avatar image.
        author_badges_url (TextField): URL to the author's badges.
        community_id (UUIDField): Identifier for the associated community.
        sport (ForeignKey): The sport associated with the event.
        title (CharField): Title of the event.
        description (TextField): Description of the event.
        is_pinned (BooleanField): Indicates if the event is pinned.
        location_name (CharField): Name of the event location.
        location_lat (DecimalField): Latitude of the event location.
        location_lng (DecimalField): Longitude of the event location.
        start_time (DateTimeField): Start time of the event.
        end_time (DateTimeField): End time of the event.
        fee (BigIntegerField): Fee for attending the event.
        total_click (BigIntegerField): Number of times the event has been clicked.
        created_at (DateTimeField): Timestamp when the event was created.
        updated_at (DateTimeField): Timestamp when the event was last updated.
    Meta:
        Ensures only one event can be pinned at a time using a unique constraint.
    Methods:
        save(): If the event is pinned, unpins all other events before saving.
        __str__(): Returns the title of the event.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_display_name = models.CharField(max_length=80, blank=True, null=True)
    author_avatar_url = models.TextField(blank=True, null=True)
    author_badges_url = models.TextField(blank=True, null=True)
    community_id = models.UUIDField(null=True, blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    location_name = models.CharField(max_length=120, blank=True, null=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    fee = models.BigIntegerField(null=True, blank=True)
    total_click = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        """
        Meta class for model constraints.
        This Meta class defines a unique constraint on the 'is_pinned' field, ensuring that only one instance can have 'is_pinned=True' at any given time. This is useful for scenarios where only one event or object should be marked as pinned.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['is_pinned'],
                condition=Q(is_pinned=True),
                name='unique_pinned_event'
            )
        ]

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure only one event can be pinned at a time.
        """
        if self.is_pinned:
            Event.objects.exclude(pk=self.pk).filter(is_pinned=True).update(is_pinned=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserEvent(models.Model):
    """
    Represents the association between a User and an Event.
    This model tracks which users are linked to which events, along with the timestamp
    when the association was created. Each user-event pair is unique.
    Attributes:
        user (ForeignKey): Reference to the User participating in the event.
        event (ForeignKey): Reference to the Event the user is associated with.
        created_at (DateTimeField): Timestamp when the association was created.
    Meta:
        unique_together: Ensures that each (user, event) pair is unique.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "event")

class EventImage(models.Model):
    """
    Model representing an image associated with an event.
    Attributes:
        id (UUIDField): Unique identifier for the image.
        event (ForeignKey): Reference to the related Event object.
        image (CloudinaryField): Image file stored in Cloudinary, validated for size, optional.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField("image", validators=[validate_image_size], null=True, blank=True)
