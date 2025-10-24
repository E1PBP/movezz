from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "condition", "location", "owner", "is_active", "created_at")
    list_filter  = ("condition", "is_active", "location", "created_at")
    search_fields = ("title", "description", "location", "owner__username")
    readonly_fields = ("created_at",)
    exclude = ("owner",)  

    def save_model(self, request, obj, form, change):
        if not change and not obj.owner_id:
            obj.owner = request.user   
        super().save_model(request, obj, form, change)