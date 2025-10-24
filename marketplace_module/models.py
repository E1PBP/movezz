import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from common.models import Sport
from common.choices import ListingCondition
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size

class Listing(models.Model):
    class Condition(models.TextChoices):
        BRAND_NEW = "BRAND_NEW", "Brand New"
        USED = "USED", "Used"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings",
        null=True, blank=True,
        db_column="seller_id", 
    )

    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.PositiveIntegerField()
    condition = models.CharField(max_length=10, choices=Condition.choices)
    location = models.CharField(max_length=120)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    wishlisted_by = models.ManyToManyField(
        User,
        related_name="wishlisted_listings",
        blank=True,
        through="Wishlist",
        through_fields=("listing", "user"),
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def seller(self): return self.owner
    @seller.setter
    def seller(self, v): self.owner = v
    @property
    def seller_id(self): return self.owner_id
    @seller_id.setter
    def seller_id(self, v): self.owner_id = v

class ListingImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(Listing, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField("image", validators=[validate_image_size], null=True, blank=True)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "listing"], name="uniq_user_listing_wishlist"),
        ]