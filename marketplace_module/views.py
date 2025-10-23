from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.core import serializers
from django.urls import reverse
import json, uuid  
from marketplace_module.models import Listing, Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from decimal import Decimal, InvalidOperation

# show today's pick page
def todays_pick(request):
    placeholder_uuid = uuid.UUID("00000000-0000-0000-0000-000000000000")
    
    page_configuration = {
        "isAuthenticated": request.user.is_authenticated,
        "apiListings": reverse("marketplace_module:get_listings"),
        "detailUrlPattern": reverse("marketplace_module:listing_detail",kwargs={"listing_id": placeholder_uuid}),
        "currentUserId": request.user.id if request.user.is_authenticated else None,
        "wishlistIdsUrl": reverse("marketplace_module:wishlist_ids"),
        "wishlistToggleUrl": reverse("marketplace_module:wishlist_toggle"),
        "apiWishlistListings": reverse("marketplace_module:wishlist_listings"),
        "apiToggleWishlist": reverse("marketplace_module:wishlist_toggle"),
    }
    
    context = {
        "page_config_json": json.dumps(page_configuration)
    }
    
    return render(request, "todays_pick.html", context)

# show detail page
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id, is_active=True)

    context = {
        "listing": listing
    }
    return render(request, "listing_detail.html", context)

# create listing with AJAX
@csrf_exempt
@require_POST
@login_required
def add_listing_entry_ajax(request):
    """
    Create a Listing via AJAX (Tutorial-5 style).
    Returns 201 on success and dispatch 'listing:created' on client.
    """
    try:
        title = strip_tags(request.POST.get("title", "")).strip()
        description = strip_tags(request.POST.get("description", "")).strip()
        location = request.POST.get("location", "").strip()
        image_url = request.POST.get("image_url", "").strip()
        condition = request.POST.get("condition", "").strip()
        price_raw = request.POST.get("price", "").strip()

        if not title:
            return HttpResponseBadRequest("Title is required")

        if condition not in ("BRAND_NEW", "USED"):
            return HttpResponseBadRequest("Invalid condition")

        try:
            price = Decimal(price_raw or "0")
            if price < 0:
                return HttpResponseBadRequest("Price must be >= 0")
        except (InvalidOperation, TypeError):
            return HttpResponseBadRequest("Invalid price")

        listing = Listing.objects.create(
            owner=request.user,        
            title=title,
            description=description,
            location=location,
            image_url=image_url,
            condition=condition,
            price=price,
            is_active=True,
        )
        return HttpResponse(b"CREATED", status=201)

    except Exception as e:
        return JsonResponse({"error": "exception", "message": str(e)}, status=500)

# to get listings
@require_GET
def get_listings(request):
    VALID_CONDITIONS = ("BRAND_NEW", "USED")
    
    listings_queryset = Listing.objects.filter(is_active=True)

    # search filter
    search_query = request.GET.get("q", "").strip()
    if search_query:
        listings_queryset = listings_queryset.filter(title__icontains=search_query)

    # condition filter
    condition_filter = request.GET.get("condition")
    if condition_filter in VALID_CONDITIONS:
        listings_queryset = listings_queryset.filter(condition=condition_filter)

    # serialize to JSON
    serialized_listings = serializers.serialize(
        "json",
        listings_queryset,
        fields=("title", "price", "condition", "location", "image_url"),
    )
    
    return HttpResponse(serialized_listings, content_type="application/json")

# get listing detail
@require_GET
def get_listing_detail(request, listing_id):
    listing_queryset = Listing.objects.filter(pk=listing_id, is_active=True)
    
    if not listing_queryset.exists():
        return JsonResponse({"detail": "Not found"}, status=404)

    serialized_listing = serializers.serialize(
        "json",
        listing_queryset,
        fields=("title", "price", "condition", "location", "image_url", "description"),
    )
    
    return HttpResponse(serialized_listing, content_type="application/json")

# show wishlist page
@login_required
def wishlist_page(request):
    config = {
        "isAuthenticated": True,
        "detailUrlPattern": reverse(
            "marketplace_module:listing_detail",
            args=["00000000-0000-0000-0000-000000000000"],
        ),
        "apiWishlistListings": reverse("marketplace_module:wishlist_listings"),
        "apiToggleWishlist": reverse("marketplace_module:wishlist_toggle"),
    }
    return render(
        request,
        "wishlist.html",
        {"page_config_json": json.dumps(config)},
    )

# get wishlist ids
@login_required
@require_GET
def wishlist_ids(request):
    """Return an array of listing ids the current user saved."""
    from marketplace_module.models import Wishlist  # no DB changes, just import
    ids = list(
        Wishlist.objects.filter(user=request.user)
        .values_list("listing__id", flat=True)
    )
    return JsonResponse(ids, safe=False)

# get wishlist listings
@login_required
@require_GET
def wishlist_listings(request):
    """Return serialized listings the user saved (Django serializer shape)."""
    from marketplace_module.models import Wishlist, Listing
    listing_ids = Wishlist.objects.filter(user=request.user)\
                                  .values_list("listing_id", flat=True)
    qs = Listing.objects.filter(pk__in=listing_ids, is_active=True)
    data = serializers.serialize(
        "json",
        qs,
        fields=("title", "price", "condition", "location", "image_url"),
    )
    return HttpResponse(data, content_type="application/json")

#get toggle wishlist
@csrf_exempt
@require_POST
@login_required
def wishlist_toggle(request):
    """
    POST body: listing_id
    Response: {"status": "added" | "removed", "id": "<uuid>"}
    """
    from marketplace_module.models import Wishlist, Listing
    listing_id = request.POST.get("listing_id")
    if not listing_id:
        return JsonResponse({"error": "missing_listing_id"}, status=400)

    listing = get_object_or_404(Listing, pk=listing_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, listing=listing)
    if created:
        return JsonResponse({"status": "added", "id": str(listing.pk)})
    obj.delete()
    return JsonResponse({"status": "removed", "id": str(listing.pk)})