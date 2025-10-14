from django.contrib import admin
from .models import Listing, ListingImage, ListingReview
# Register your models here.
admin.site.register(Listing)
admin.site.register(ListingImage)
admin.site.register(ListingReview)