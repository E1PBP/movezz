import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from common.models import Sport
from common.choices import ListingCondition
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size


class Listing(models.Model):
    '''Model representing a marketplace listing.'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_display_name = models.CharField(max_length=80, blank=True, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    listing_type = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=20, choices=ListingCondition.choices, default=ListingCondition.BRAND_NEW)
    location = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class ListingImage(models.Model):
    '''Model representing an image associated with a listing.'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField("image", validators=[validate_image_size], null=True, blank=True)

class ListingReview(models.Model):
    '''Model representing a review for a listing.'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class Meta:
    unique_together = ("listing", "reviewer")
