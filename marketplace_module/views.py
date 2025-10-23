from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.core import serializers
from django.urls import reverse
import json
import uuid

from marketplace_module.models import Listing, Wishlist

def todays_pick(request):
    placeholder_uuid = uuid.UUID("00000000-0000-0000-0000-000000000000")
    
    page_configuration = {
        "isAuthenticated": request.user.is_authenticated,
        "apiListings": reverse("marketplace_module:api_listings"),
        "detailUrlPattern": reverse(
            "marketplace_module:listing_detail",
            kwargs={"listing_id": placeholder_uuid}
        ),
        "wishlistIdsUrl": reverse("marketplace_module:api_wishlist_ids"),
        "wishlistToggleUrl": reverse("marketplace_module:api_wishlist_toggle"),
    }
    
    context = {
        "page_config_json": json.dumps(page_configuration)
    }
    
    return render(request, "todays_pick.html", context)


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, is_active=True)

    context = {
        "listing": listing
    }
    return render(request, "listing_detail.html", context)


@login_required
def wishlist(request):
    user_wishlist_items = Listing.objects.filter(
        wishlisted_by=request.user
    ).prefetch_related("wishlisted_by")

    context = {
        'wishlist_items': user_wishlist_items,
    }
    return render(request, 'wishlist.html', context)


def show_json(request):
    all_listings = Listing.objects.all()
    listings_data = [
        {
            'id': str(listing.id),
            'title': listing.title,
            'price': str(listing.price),
            'condition': listing.condition,
            'location': listing.location,
            'description': listing.description,
            'image_url': listing.image_url,
        }
        for listing in all_listings
    ]
    return JsonResponse(listings_data, safe=False)


def show_json_by_id(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    listing_data = {
        'id': str(listing.id),
        'title': listing.title,
        'price': str(listing.price),
        'condition': listing.condition,
        'location': listing.location,
        'description': listing.description,
        'image_url': listing.image_url,
    }
    return JsonResponse(listing_data)


@require_GET
def api_listings(request):
    VALID_CONDITIONS = ("BRAND_NEW", "USED")
    
    listings_queryset = Listing.objects.filter(is_active=True)

    # Apply search filter
    search_query = request.GET.get("q", "").strip()
    if search_query:
        listings_queryset = listings_queryset.filter(title__icontains=search_query)

    # Apply condition filter
    condition_filter = request.GET.get("condition")
    if condition_filter in VALID_CONDITIONS:
        listings_queryset = listings_queryset.filter(condition=condition_filter)

    # Serialize and return limited results
    serialized_listings = serializers.serialize(
        "json",
        listings_queryset,
        fields=("title", "price", "condition", "location", "image_url"),
    )
    
    return HttpResponse(serialized_listings, content_type="application/json")


@require_GET
def api_listing_detail(request, listing_id):
    listing_queryset = Listing.objects.filter(pk=listing_id, is_active=True)
    
    if not listing_queryset.exists():
        return JsonResponse({"detail": "Not found"}, status=404)

    serialized_listing = serializers.serialize(
        "json",
        listing_queryset,
        fields=("title", "price", "condition", "location", "image_url", "description"),
    )
    
    return HttpResponse(serialized_listing, content_type="application/json")


@require_GET
@login_required
def api_wishlist_ids(request):
    wishlist_listing_ids = list(
        Wishlist.objects.filter(user=request.user)
        .values_list("listing_id", flat=True)
    )
    
    return JsonResponse(wishlist_listing_ids, safe=False)


@require_POST
@login_required
def api_wishlist_toggle(request):
    listing_id = request.POST.get("listing_id")
    
    if not listing_id:
        return HttpResponseBadRequest("Missing listing_id parameter")
    
    listing = get_object_or_404(Listing, pk=listing_id, is_active=True)
    
    wishlist_item, was_created = Wishlist.objects.get_or_create(
        user=request.user, 
        listing=listing
    )
    
    if was_created:
        return JsonResponse({"saved": True})
    else:
        wishlist_item.delete()
        return JsonResponse({"saved": False})