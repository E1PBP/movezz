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
        update_following_count(): Updates the following count based on Follow relationships.
        update_followers_count(): Updates the followers count based on Follow relationships.
        update_all_counts(): Updates both following and followers counts.

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
    
    def update_following_count(self) -> None:
        self.following_count = Follow.objects.filter(follower=self.user).count()
        self.updated_at = timezone.now()
        self.save(update_fields=['following_count', 'updated_at'])
    
    def update_followers_count(self) -> None:
        self.followers_count = Follow.objects.filter(followee=self.user).count()
        self.updated_at = timezone.now()
        self.save(update_fields=['followers_count', 'updated_at'])
    
    def update_all_counts(self) -> None:
        self.following_count = Follow.objects.filter(follower=self.user).count()
        self.followers_count = Follow.objects.filter(followee=self.user).count()
        self.updated_at = timezone.now()
        self.save(update_fields=['following_count', 'followers_count', 'updated_at'])

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

    def save(self, *args, **kwargs) -> None:
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            try:
                follower_profile = Profile.objects.get(user=self.follower)
                follower_profile.update_following_count()
            except Profile.DoesNotExist:
                pass
            
            try:
                followee_profile = Profile.objects.get(user=self.followee)
                followee_profile.update_followers_count()
            except Profile.DoesNotExist:
                pass

    def delete(self, *args, **kwargs) -> None:
        follower_user = self.follower
        followee_user = self.followee
        
        super().delete(*args, **kwargs)
        
        try:
            follower_profile = Profile.objects.get(user=follower_user)
            follower_profile.update_following_count()
        except Profile.DoesNotExist:
            pass
        
        try:
            followee_profile = Profile.objects.get(user=followee_user)
            followee_profile.update_followers_count()
        except Profile.DoesNotExist:
            pass

    class Meta:
        unique_together = ("follower", "followee")

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "badge")
