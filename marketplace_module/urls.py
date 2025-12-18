from django.urls import path
from django.http import HttpResponse
from . import views

app_name = 'marketplace_module'

urlpatterns = [
    path("todays-pick/", views.todays_pick, name="todays_pick"),
    path("listing/<uuid:listing_id>/", views.listing_detail, name="listing_detail"),
    path("wishlist/", views.wishlist_page, name="wishlist_page"),
    path("api/listings/", views.get_listings, name="get_listings"),                 
    path("api/listings/<uuid:listing_id>/", views.get_listing_detail, name="get_listing_detail"),
    path("api/wishlist/ids/", views.wishlist_ids, name="wishlist_ids"),
    path("api/wishlist/list/", views.wishlist_listings, name="wishlist_listings"),
    path("api/wishlist/toggle/", views.wishlist_toggle, name="wishlist_toggle"),
    path("api/listings/create-ajax/", views.add_listing_entry_ajax,name="add_listing_entry_ajax"),
    path("listing/<uuid:listing_id>/edit-ajax/", views.edit_listing_entry_ajax, name="edit_listing_entry_ajax"),
    path("listing/<uuid:listing_id>/delete-ajax/", views.delete_listing_entry_ajax, name="delete_listing_entry_ajax"),
    path("proxy-image/", views.proxy_image, name="proxy_image"),
]