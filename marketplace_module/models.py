import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from common.models import Sport
from common.choices import ListingCondition
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size


class Listing(models.Model):
    """
    Represents a listing in the marketplace.
    Attributes:
        id (UUIDField): A unique identifier for the listing.
        seller (ForeignKey): The user who is selling the item.
        seller_display_name (CharField): The display name of the seller.
        sport (ForeignKey): The sport associated with the listing.
        title (CharField): The title of the listing.
        description (TextField): A description of the item being listed.
        listing_type (CharField): The type of listing (e.g., "Equipment", "Service").
        price (DecimalField): The price of the item.
        condition (CharField): The condition of the item (e.g., "New", "Used").
        location (CharField): The location where the item is available.
        created_at (DateTimeField): The date and time the listing was created.
        updated_at (DateTimeField): The date and time the listing was last updated.
    """
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
    """Model representing an image associated with a listing.
    Attributes:
        id (UUIDField): The unique identifier for the image.
        listing (ForeignKey): The listing to which the image belongs.
        image (CloudinaryField): The image file stored on Cloudinary.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField("image", validators=[validate_image_size], null=True, blank=True)

class ListingReview(models.Model):
    """
    Model representing a review for a listing.
    Attributes:
        id (UUIDField): The unique identifier for the review.
        listing (ForeignKey): The listing being reviewed.
        reviewer (ForeignKey): The user who wrote the review.
        rating (SmallIntegerField): The rating given to the listing (e.g., 1-5).
        comment (TextField): Optional comments about the listing.
        created_at (DateTimeField): The date and time the review was created.
    Meta:
        unique_together (tuple): Ensures that a user can only review a listing once.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("listing", "reviewer")
