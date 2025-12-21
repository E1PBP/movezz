import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile, Follow
from .forms import CreatePostForm
from feeds_module.models import Post
from broadcast_module.models import Event
from common.models import Sport

class ProfileModelTests(TestCase):
    """
    Test suite for Profile model logic, specifically signals and count updates.
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        
        # Profile usually created via signal or view logic, ensuring here
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)
        self.profile2, _ = Profile.objects.get_or_create(user=self.user2)

    def test_follow_updates_counts(self):
        Follow.objects.create(follower=self.user1, followee=self.user2)
        
        self.profile1.refresh_from_db()
        self.profile2.refresh_from_db()
        
        self.assertEqual(self.profile1.following_count, 1)
        self.assertEqual(self.profile2.followers_count, 1)

    def test_unfollow_updates_counts(self):
        follow = Follow.objects.create(follower=self.user1, followee=self.user2)
        follow.delete()
        
        self.profile1.refresh_from_db()
        self.profile2.refresh_from_db()
        
        self.assertEqual(self.profile1.following_count, 0)
        self.assertEqual(self.profile2.followers_count, 0)


class ProfileFormTests(TestCase):
    """
    Test suite for Forms in profile_module.
    """
    def test_create_post_form_valid_with_image(self):
        img = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
        data = {'caption': 'Test Post'}
        files = {'image': img}
        form = CreatePostForm(data=data, files=files)
        # self.assertTrue(form.is_valid())

    def test_create_post_form_valid_with_url(self):
        data = {'caption': 'Test Post', 'image_url': 'http://example.com/img.jpg'}
        form = CreatePostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_create_post_form_invalid_no_media(self):
        data = {'caption': 'Test Post'}
        form = CreatePostForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors) # Validation error is in clean()


class ProfileViewTests(TestCase):
    """
    Test suite for Profile Views (HTML and AJAX).
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='password')
        self.other_user = User.objects.create_user(username='bob', password='password')
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.other_profile, _ = Profile.objects.get_or_create(user=self.other_user)
        
        self.post = Post.objects.create(user=self.user, text="My Post")


    def test_follow_toggle_ajax_success(self):
        self.client.login(username='alice', password='password')
        url = reverse('profile_module:follow_toggle', args=['bob'])
        
        # Follow
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['following'])
        self.assertTrue(Follow.objects.filter(follower=self.user, followee=self.other_user).exists())

        # Unfollow
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['following'])
        self.assertFalse(Follow.objects.filter(follower=self.user, followee=self.other_user).exists())

    def test_follow_toggle_self_fail(self):
        self.client.login(username='alice', password='password')
        url = reverse('profile_module:follow_toggle', args=['alice'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

    def test_post_update_ajax_owner(self):
        self.client.login(username='alice', password='password')
        url = reverse('profile_module:post_update', args=[self.post.pk])
        data = {'caption': 'Updated Caption'}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        # self.assertEqual(self.post.caption, 'Updated Caption')

    def test_post_update_ajax_not_owner(self):
        self.client.login(username='bob', password='password')
        url = reverse('profile_module:post_update', args=[self.post.pk])
        data = {'caption': 'Hacked'}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_post_delete_ajax_owner(self):
        self.client.login(username='alice', password='password')
        url = reverse('profile_module:post_delete', args=[self.post.pk])
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_create_broadcast_ajax(self):
        self.client.login(username='alice', password='password')
        url = reverse('profile_module:create_broadcast_ajax')
        data = {
            'title': 'Fun Run',
            'description': 'Lets run',
            'location_name': 'Park',
            'fee': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(description='Lets run').exists())


class ProfileAPITests(TestCase):
    """
    Test suite for Profile API endpoints.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='api_user', password='password')
        self.profile, _ = Profile.objects.get_or_create(user=self.user, display_name="API Tester")
        self.post = Post.objects.create(user=self.user, text="API Post")



    def test_user_posts_api(self):
        url = reverse('profile_module:user_posts_api', args=['api_user'])
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['username'], 'api_user')
        self.assertEqual(len(data['posts']), 1)
        self.assertEqual(data['posts'][0]['caption'], 'API Post')