import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Listing, Wishlist

class MarketplaceModelTests(TestCase):
    """
    Test suite untuk Model Marketplace (Listing & Wishlist).
    """
    def setUp(self):
        self.user = User.objects.create_user(username='seller', password='password')
        self.listing = Listing.objects.create(
            owner=self.user,
            title='Test Item',
            description='Description',
            price=100000,
            condition='BRAND_NEW',
            location='Jakarta',
            image_url='http://example.com/image.jpg'
        )

    def test_listing_creation(self):
        self.assertEqual(self.listing.title, 'Test Item')
        self.assertEqual(self.listing.owner, self.user)
        self.assertTrue(self.listing.is_active)

    def test_wishlist_creation(self):
        buyer = User.objects.create_user(username='buyer', password='password')
        wishlist = Wishlist.objects.create(user=buyer, listing=self.listing)
        self.assertEqual(wishlist.user, buyer)
        self.assertEqual(wishlist.listing, self.listing)


class MarketplaceViewTests(TestCase):
    """
    Test suite untuk Views berbasis HTML (Todays Pick, Detail, Wishlist Page).
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.listing = Listing.objects.create(
            owner=self.user,
            title='HTML Item',
            description='Desc',
            price=50000,
            condition='USED',
            location='Depok'
        )
        self.todays_pick_url = reverse('marketplace_module:todays_pick')
        self.wishlist_page_url = reverse('marketplace_module:wishlist_page')
        self.detail_url = reverse('marketplace_module:listing_detail', args=[self.listing.id])

    def test_todays_pick_view(self):
        # Login agar navbar tidak error saat render URL profile (username required)
        self.client.login(username='user', password='password')
        response = self.client.get(self.todays_pick_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todays_pick.html')

    def test_listing_detail_view(self):
        # Login agar navbar tidak error
        self.client.login(username='user', password='password')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listing_detail.html')
        self.assertEqual(response.context['listing'], self.listing)

    def test_listing_detail_not_found(self):
        # Login diperlukan karena halaman 404 juga me-render navbar yang butuh username
        self.client.login(username='user', password='password')
        import uuid
        url = reverse('marketplace_module:listing_detail', args=[uuid.uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_wishlist_page_authenticated(self):
        self.client.login(username='user', password='password')
        response = self.client.get(self.wishlist_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')

    def test_wishlist_page_unauthenticated(self):
        # Redirect ke login page biasanya tidak merender template navbar, jadi aman tanpa login
        response = self.client.get(self.wishlist_page_url)
        self.assertEqual(response.status_code, 302)


class MarketplaceAPITests(TestCase):
    """
    Test suite untuk API/AJAX Endpoints (CRUD, Filter, Wishlist).
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='api_user', password='password')
        self.other_user = User.objects.create_user(username='other', password='password')
        
        self.listing = Listing.objects.create(
            owner=self.user,
            title='API Item',
            description='API Desc',
            price=150000,
            condition='BRAND_NEW',
            location='Bogor',
            is_active=True
        )
        
        self.create_url = reverse('marketplace_module:add_listing_entry_ajax')
        self.list_url = reverse('marketplace_module:get_listings')
        self.wishlist_toggle_url = reverse('marketplace_module:wishlist_toggle')

    # --- LISTING CRUD TESTS ---

    def test_get_listings_api(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['title'], 'API Item')

    def test_get_listings_search_filter(self):
        Listing.objects.create(owner=self.other_user, title='Other Item', price=100, condition='USED', location='X')
        
        response = self.client.get(self.list_url, {'q': 'API'})
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['title'], 'API Item')

    def test_get_listings_condition_filter(self):
        Listing.objects.create(owner=self.other_user, title='Used Item', price=100, condition='USED', location='X')
        
        response = self.client.get(self.list_url, {'condition': 'USED'})
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['title'], 'Used Item')

    def test_create_listing_success(self):
        self.client.login(username='api_user', password='password')
        data = {
            'title': 'New Listing',
            'description': 'New Desc',
            'price': '200000',
            'condition': 'BRAND_NEW',
            'location': 'Jakarta',
            'image_url': 'http://test.com/img.png'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Listing.objects.filter(title='New Listing').exists())

    def test_create_listing_invalid_price(self):
        self.client.login(username='api_user', password='password')
        data = {
            'title': 'Bad Price',
            'price': '-100',
            'condition': 'BRAND_NEW'
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 400)

    def test_edit_listing_owner_success(self):
        self.client.login(username='api_user', password='password')
        url = reverse('marketplace_module:edit_listing_entry_ajax', args=[self.listing.id])
        data = {
            'title': 'Updated Title',
            'description': 'Updated Desc',
            'price': '300000',
            'condition': 'USED',
            'location': 'Bogor',
            'image_url': ''
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, 'Updated Title')
        self.assertEqual(self.listing.price, 300000)

    def test_edit_listing_not_owner_fail(self):
        self.client.login(username='other', password='password')
        url = reverse('marketplace_module:edit_listing_entry_ajax', args=[self.listing.id])
        data = {'title': 'Hacked'}
        
        # Expect 500 or 404 depending on view implementation of exception handling
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [404, 500])
        
        self.listing.refresh_from_db()
        self.assertNotEqual(self.listing.title, 'Hacked')

    def test_delete_listing_success(self):
        self.client.login(username='api_user', password='password')
        url = reverse('marketplace_module:delete_listing_entry_ajax', args=[self.listing.id])
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Listing.objects.filter(id=self.listing.id).exists())

    # --- WISHLIST TESTS ---

    def test_wishlist_toggle_add_remove(self):
        self.client.login(username='api_user', password='password')
        
        # 1. Add to wishlist
        response = self.client.post(self.wishlist_toggle_url, {'listing_id': self.listing.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'added')
        self.assertTrue(Wishlist.objects.filter(user=self.user, listing=self.listing).exists())

        # 2. Remove from wishlist
        response = self.client.post(self.wishlist_toggle_url, {'listing_id': self.listing.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'removed')
        self.assertFalse(Wishlist.objects.filter(user=self.user, listing=self.listing).exists())

    def test_wishlist_ids_api(self):
        self.client.login(username='api_user', password='password')
        Wishlist.objects.create(user=self.user, listing=self.listing)
        
        url = reverse('marketplace_module:wishlist_ids')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(str(self.listing.id), [str(id) for id in data])

    def test_wishlist_listings_api(self):
        self.client.login(username='api_user', password='password')
        Wishlist.objects.create(user=self.user, listing=self.listing)
        
        url = reverse('marketplace_module:wishlist_listings')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], str(self.listing.id))