from django.urls import path
from django.http import HttpResponse
from . import views

app_name = 'marketplace_module'

urlpatterns = [
    path('', views.todays_pick, name='todays_pick'),
    path("todays-pick/", views.todays_pick, name="todays_pick"),
    path("listing/<uuid:listing_id>/", views.listing_detail, name="listing_detail"),
    path("api/listings/", views.api_listings, name="api_listings"),
    path("api/listings/<uuid:listing_id>/", views.api_listing_detail, name="api_listing_detail"),
    path("api/wishlist/ids/", views.api_wishlist_ids, name="api_wishlist_ids"),
    path("api/wishlist/toggle/", views.api_wishlist_toggle, name="api_wishlist_toggle"),
]

