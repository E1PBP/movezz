from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class AuthViewsTest(TestCase):
    """ Tests for authentication views: login, register, logout.
    Args:
        TestCase : Django test case class for simulating requests and checking responses.
    """
    
    
    def setUp(self):
        """ Set up test user and URLs.
        This method is called before each test function to set up any state specific to the test.
        
        Args:
            None
        Returns:
            None
        """
        self.login_url = reverse('auth_module:login')
        self.register_url = reverse('auth_module:register')
        self.logout_url = reverse('auth_module:logout')


        self.username = 'testuser'
        self.password = 'safepassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_get_shows_form(self):
        """ Test GET request to login view shows the login form.
        Args:
            None
        Returns:
            None
        """
        resp = self.client.get(self.login_url)
        self.assertEqual(resp.status_code, 200)

        self.assertIn('form', resp.context)

    def test_login_post_valid_credentials_logs_in_and_redirects(self):
        """
        Test POST request to login view with valid credentials logs in the user and redirects.
        Args:
            None
        Returns:
            None
        """
        resp = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
        })

        self.assertEqual(resp.status_code, 302)

        self.assertIn('_auth_user_id', self.client.session)

    def test_login_post_invalid_credentials_shows_errors(self):
        """
        Test POST request to login view with invalid credentials shows form errors.
        Args:    
            None
        Returns:
            None
        """
        resp = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword',
        })

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

        form = resp.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.non_field_errors())

    def test_register_post_creates_user_and_logs_in(self):
        """
        Test POST request to register view creates a new user and logs them in.
        Args:
            None
        Returns:
            None
        """
        new_username = 'newuser'
        new_password = 'newpass12345'

        self.assertFalse(User.objects.filter(username=new_username).exists())

        resp = self.client.post(self.register_url, {
            'username': new_username,
            'password1': new_password,
            'password2': new_password,
        })

        self.assertEqual(resp.status_code, 302)

        self.assertTrue(User.objects.filter(username=new_username).exists())

        self.assertIn('_auth_user_id', self.client.session)

    def test_authenticated_user_getting_login_or_register_redirects(self):
        """
        Test that an authenticated user trying to access login or register views gets redirected.
        Args:
            None
        Returns:
            None
        """
        self.client.login(username=self.username, password=self.password)

        resp = self.client.get(self.login_url)

        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(self.register_url)
        self.assertEqual(resp.status_code, 302)

    def test_logout_requires_login_and_logs_out(self):
        """
        Test that logout view requires login and logs out the user.
        Args:
            None
        Returns:
            None
        """
        resp = self.client.get(self.logout_url)
        self.assertEqual(resp.status_code, 302)

        self.assertIn('login', resp['Location'])


        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        resp = self.client.get(self.logout_url)
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
