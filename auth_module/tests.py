import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm

class AuthFormTests(TestCase):
    """
    Testing validasi pada Form Django (LoginForm dan RegisterForm).
    """
    def test_register_form_valid(self):
        data = {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_register_form_password_mismatch(self):
        data = {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'mismatch123',
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_login_form_valid(self):
        User.objects.create_user(username='someuser', password='somepassword')
        
        data = {
            'username': 'someuser',
            'password': 'somepassword'
        }

        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())


class AuthHTMLViewTests(TestCase):
    """
    Testing Views berbasis HTML (Login, Register, Logout).
    """
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('auth_module:login')
        self.register_url = reverse('auth_module:register')
        self.logout_url = reverse('auth_module:logout')
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_view_template_used(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_view_template_used(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_authenticated_user_redirect(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('feeds_module:main_view'))

    def test_register_authenticated_user_redirect(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.register_url)
        self.assertRedirects(response, reverse('feeds_module:main_view'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertNotIn('_auth_user_id', self.client.session)


class AuthAPITests(TestCase):
    """
    Testing Endpoint API (JSON) untuk kebutuhan Mobile/Frontend.
    """
    def setUp(self):
        self.client = Client()
        self.api_login_url = reverse('auth_module:api_login')
        self.api_register_url = reverse('auth_module:api_register')
        self.api_logout_url = reverse('auth_module:api_logout')
        self.api_me_url = reverse('auth_module:me_api')
        
        self.user = User.objects.create_user(
            username='apiuser', 
            password='apipassword', 
            email='api@test.com',
            first_name='Api',
            last_name='User'
        )

    def test_api_register_success(self):
        payload = {
            'username': 'mobileuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        response = self.client.post(
            self.api_register_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['status'])
        self.assertEqual(data['message'], "User created successfully!")
        self.assertTrue(User.objects.filter(username='mobileuser').exists())

    def test_api_register_password_mismatch(self):
        payload = {
            'username': 'mobileuser2',
            'password1': 'pass123',
            'password2': 'differentpass'
        }
        response = self.client.post(
            self.api_register_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['status'])

    def test_api_register_username_taken(self):
        payload = {
            'username': 'apiuser',
            'password1': 'pass123',
            'password2': 'pass123'
        }
        response = self.client.post(
            self.api_register_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], "Username already exists.")

    def test_api_register_invalid_method(self):
        response = self.client.get(self.api_register_url)
        self.assertEqual(response.status_code, 400)

    def test_api_login_success(self):
        response = self.client.post(self.api_login_url, {
            'username': 'apiuser',
            'password': 'apipassword'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['status'])
        self.assertEqual(data['username'], 'apiuser')
        self.assertIn('_auth_user_id', self.client.session)

    def test_api_login_invalid_credentials(self):
        response = self.client.post(self.api_login_url, {
            'username': 'apiuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json()['status'])

    def test_api_login_inactive_user(self):
        inactive_user = User.objects.create_user(username='inactive', password='pwd')
        inactive_user.is_active = False
        inactive_user.save()

        response = self.client.post(self.api_login_url, {
            'username': 'inactive',
            'password': 'pwd'
        })
        

        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data['status'])

        self.assertIn("Login failed", data['message'])

    def test_api_logout_success(self):
        self.client.login(username='apiuser', password='apipassword')
        response = self.client.post(self.api_logout_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['status'])
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_api_me_authenticated(self):
        self.client.login(username='apiuser', password='apipassword')
        response = self.client.get(self.api_me_url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['status'])
        self.assertEqual(data['username'], 'apiuser')

    def test_api_me_unauthenticated(self):
        response = self.client.get(self.api_me_url)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json()['status'])