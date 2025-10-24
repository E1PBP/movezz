from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event
from django.utils import timezone
from profile_module.models import Profile

User = get_user_model()

class BroadcastModuleTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='user1', password='testpass', first_name='Test', last_name='User')
		self.staff = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
		start_dt = timezone.now() + timezone.timedelta(days=1)
		end_dt = timezone.now() + timezone.timedelta(days=1, hours=2)
		self.event_data = {
			'description': 'Test Event',
			'start_time': start_dt.strftime('%Y-%m-%dT%H:%M'),
			'end_time': end_dt.strftime('%Y-%m-%dT%H:%M'),
			'location_name': 'Test Location',
			'fee': '0',
			'rsvp_url': 'https://example.com',
		}

	def test_event_creation_authenticated(self):
		self.client.login(username='user1', password='testpass')
		response = self.client.post(reverse('broadcast_module:create'), self.event_data)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(Event.objects.filter(description='Test Event').exists())

	def test_event_creation_unauthenticated(self):
		response = self.client.post(reverse('broadcast_module:create'), self.event_data)
		self.assertEqual(response.status_code, 401)

	def test_event_creation_missing_required(self):
		self.client.login(username='user1', password='testpass')
		data = self.event_data.copy()
		data.pop('start_time')
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 400)

	def test_trending_events_endpoint(self):
		start_dt = timezone.now() + timezone.timedelta(days=1)
		end_dt = timezone.now() + timezone.timedelta(days=1, hours=2)
		Event.objects.create(
			user=self.user, 
			author_display_name='User',
			description='Test Event',
			start_time=start_dt,
			end_time=end_dt,
			location_name='Test Location',
			fee=0,
			rsvp_url='https://example.com'
		)
		url = reverse('broadcast_module:trending')
		response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)
		self.assertIn('html', response.json())

	def test_latest_events_endpoint(self):
		start_dt = timezone.now() + timezone.timedelta(days=1)
		end_dt = timezone.now() + timezone.timedelta(days=1, hours=2)
		Event.objects.create(
			user=self.user, 
			author_display_name='User',
			description='Test Event',
			start_time=start_dt,
			end_time=end_dt,
			location_name='Test Location',
			fee=0,
			rsvp_url='https://example.com'
		)
		url = reverse('broadcast_module:latest')
		response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)
		self.assertIn('html', response.json())

	def test_pin_unpin_event_admin_only(self):
		start_dt = timezone.now() + timezone.timedelta(days=1)
		end_dt = timezone.now() + timezone.timedelta(days=1, hours=2)
		event = Event.objects.create(
			user=self.user, 
			author_display_name='User',
			description='Test Event',
			start_time=start_dt,
			end_time=end_dt,
			location_name='Test Location',
			fee=0,
			rsvp_url='https://example.com'
		)
		pin_url = reverse('broadcast_module:pin', args=[event.pk])
		unpin_url = reverse('broadcast_module:unpin', args=[event.pk])
		
        # Tes apakah user non-admin bisa pin
		self.client.login(username='user1', password='testpass')
		resp = self.client.post(pin_url)
		self.assertNotEqual(resp.status_code, 200)

		# Tes apakah admin bisa pin/unpin
		self.client.login(username='admin', password='adminpass')
		resp = self.client.post(pin_url)
		self.assertEqual(resp.status_code, 200)
		event.refresh_from_db()
		self.assertTrue(event.is_pinned)
		resp = self.client.post(unpin_url)
		self.assertEqual(resp.status_code, 200)
		event.refresh_from_db()
		self.assertFalse(event.is_pinned)

	def test_click_event_increments(self):
		start_dt = timezone.now() + timezone.timedelta(days=1)
		end_dt = timezone.now() + timezone.timedelta(days=1, hours=2)
		event = Event.objects.create(
			user=self.user, 
			author_display_name='User',
			description='Test Event',
			start_time=start_dt,
			end_time=end_dt,
			location_name='Test Location',
			fee=0,
			rsvp_url='https://example.com'
		)
		url = reverse('broadcast_module:click', args=[event.pk])
		old_clicks = event.total_click
		resp = self.client.post(url)
		self.assertEqual(resp.status_code, 200)
		event.refresh_from_db()
		# Check apakah total_click terupdate
		self.assertEqual(event.total_click, old_clicks + 1)

	def test_profile_integration(self):
		# Unit test untuk mengecek apakah profile terintegrasi dalam rendered HTML
		profile, created = Profile.objects.get_or_create(
			user=self.user,
			defaults={'display_name': 'Test User', 'is_verified': True}
		)
		
		start_dt = timezone.now() + timezone.timedelta(days=1)
		end_dt = timezone.now() + timezone.timedelta(days=1, hours=2)
		Event.objects.create(
			user=self.user,
			author_display_name='User',
			description='Test Event',
			start_time=start_dt,
			end_time=end_dt,
			location_name='Test Location',
			fee=0,
			rsvp_url='https://example.com'
		)
		
		url = reverse('broadcast_module:trending')
		response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertIn('html', data)
		self.assertIn('Test User', data['html'])

	def test_coordinate_validation_invalid_latitude(self):
		self.client.login(username='user1', password='testpass')
		data = self.event_data.copy()
		data['location_lat'] = '95.0'
		data['location_lng'] = '100.0'
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 400)
		
		data['location_lat'] = '-95.0'
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 400)

	def test_coordinate_validation_invalid_longitude(self):
		self.client.login(username='user1', password='testpass')
		data = self.event_data.copy()
		data['location_lat'] = '45.0'
		data['location_lng'] = '200.0'
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 400)
		
		data['location_lng'] = '-200.0'
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 400)

	def test_coordinate_pair_requirement(self):
		self.client.login(username='user1', password='testpass')
		
		# Tanpa longitude
		data = self.event_data.copy()
		data['location_lat'] = '-6.218495'
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 400)
		
		# Tanpa lattitude
		data = self.event_data.copy()
		data['location_lng'] = '106.802445'
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 400)
		
		# Lengkap
		data = self.event_data.copy()
		data['location_lat'] = '-6.218495'
		data['location_lng'] = '106.802445'
		response = self.client.post(reverse('broadcast_module:create'), data)
		self.assertEqual(response.status_code, 200)

