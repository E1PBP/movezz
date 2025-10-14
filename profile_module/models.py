from django.db import models
from django.utils import timezone
from common.models import Sport, Badge
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size


class Profile(models.Model):
    """
    Represents a user profile in the application.
    Attributes:
        user (OneToOneField): The user associated with the profile.
        display_name (CharField): The display name of the user.
        bio (TextField): A brief biography of the user.
        link (TextField): A personal or professional link associated with the user.
        avatar_url (CloudinaryField): The URL of the user's avatar image.
        current_sport (ForeignKey): The user's current sport of interest.
        post_count (BigIntegerField): The number of posts made by the user.
        broadcast_count (BigIntegerField): The number of broadcasts made by the user.
        following_count (BigIntegerField): The number of users this user is following.
        followers_count (BigIntegerField): The number of users following this user.
        is_verified (BooleanField): Indicates if the user's profile is verified.
        created_at (DateTimeField): The date and time the profile was created.
        updated_at (DateTimeField): The date and time the profile was last updated.
    Methods:
        __str__(): Returns the display name or username of the user.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    display_name = models.CharField(max_length=80, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    avatar_url = CloudinaryField("avatar", blank=True, null=True, validators=[validate_image_size])
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
    """
    Represents the time a user has spent on a particular sport.
    Attributes:
        user (ForeignKey): The user associated with the sport.
        sport (ForeignKey): The sport associated with the user.
        time_elapsed (DurationField): The total time the user has spent on the sport.
        created_at (DateTimeField): The date and time the record was created.
    Methods:
        None
    Meta:
        unique_together: Ensures that each user-sport combination is unique.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    time_elapsed = models.DurationField(default='0')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "sport")

class Follow(models.Model):
    """
    Represents a follow relationship between two users.
    Attributes:
        follower (ForeignKey): The user who is following another user.
        followee (ForeignKey): The user being followed.
        created_at (DateTimeField): The date and time the follow relationship was created.
    Methods:
        None
    Meta:
        unique_together: Ensures that each follower-followee combination is unique.
    """
    follower = models.ForeignKey(User, related_name="follows_given", on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name="follows_received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("follower", "followee")

class UserBadge(models.Model):
    """
    Represents a badge awarded to a user.
    Attributes:
        user (ForeignKey): The user who received the badge.
        badge (ForeignKey): The badge awarded to the user.
        created_at (DateTimeField): The date and time the badge was awarded.
    Methods:
        None
    Meta:
        unique_together: Ensures that each user-badge combination is unique.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "badge")
