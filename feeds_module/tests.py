import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, PostLike, Comment, PostHashtag
from common.models import Sport, Hashtag
from profile_module.models import Profile

class FeedsModelTests(TestCase):
    """
    Test suite untuk Model di feeds_module (Post, PostLike).
    """
    def setUp(self):
        self.user = User.objects.create_user(username='modeluser', password='password')
        self.sport = Sport.objects.create(name='Soccer')

    def test_create_post(self):
        post = Post.objects.create(user=self.user, text='Test Post', sport=self.sport)
        self.assertEqual(post.text, 'Test Post')
        self.assertEqual(post.sport, self.sport)
        self.assertEqual(post.likes_count, 0)

    def test_post_like_constraint(self):

        post = Post.objects.create(user=self.user, text='Like Test')
        PostLike.objects.create(user=self.user, post=post)
        
        with self.assertRaises(Exception):
            PostLike.objects.create(user=self.user, post=post)


class FeedsViewTests(TestCase):
    """
    Test suite untuk Views HTML dan AJAX (Web Frontend).
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='feeduser', password='password')
        self.other_user = User.objects.create_user(username='other', password='password')
        
        Profile.objects.create(user=self.user, display_name="Feed User")
        Profile.objects.create(user=self.other_user, display_name="Other User")
        
        self.sport = Sport.objects.create(name='Basketball')
        self.post = Post.objects.create(user=self.other_user, text="Existing Post")
        

        self.main_url = reverse('feeds_module:main_view')
        self.create_url = reverse('feeds_module:create_post_ajax')
        self.like_url = reverse('feeds_module:like_post_ajax')
        self.comment_add_url = reverse('feeds_module:add_comment_ajax')
        self.load_more_url = reverse('feeds_module:load_more_posts')

    def test_main_view_authenticated(self):
        self.client.login(username='feeduser', password='password')
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertIn('posts', response.context)

    def test_main_view_unauthenticated(self):
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 302)

    def test_create_post_ajax_success(self):
        self.client.login(username='feeduser', password='password')
        

        data = {
            'text': 'New Ajax Post',
            'sport': 'Basketball',
            'hashtags': 'ball, game',
            'location_name': 'Gym'
        }
        
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        

        self.assertTrue(Post.objects.filter(text='New Ajax Post').exists())
        post = Post.objects.get(text='New Ajax Post')
        self.assertEqual(post.sport, self.sport)
        self.assertEqual(post.posthashtag_set.count(), 2)


    @patch('cloudinary.uploader.upload_resource')
    def test_create_post_ajax_with_image(self, mock_upload):

        mock_upload.return_value = "v12345/test_image.jpg"

        self.client.login(username='feeduser', password='password')
        img = SimpleUploadedFile("test.jpg", b"content", content_type="image/jpeg")
        data = {
            'text': 'Image Post',
            'image': img
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(text='Image Post').exists())

    def test_like_post_ajax_toggle(self):
        self.client.login(username='feeduser', password='password')
        

        response = self.client.post(self.like_url, {'post_id': self.post.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['liked'])
        self.assertEqual(data['likes_count'], 1)
        self.assertTrue(PostLike.objects.filter(user=self.user, post=self.post).exists())
        
 
        response = self.client.post(self.like_url, {'post_id': self.post.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['liked'])
        self.assertEqual(data['likes_count'], 0)
        self.assertFalse(PostLike.objects.filter(user=self.user, post=self.post).exists())

    def test_add_comment_ajax(self):
        self.client.login(username='feeduser', password='password')
        data = {'post_id': self.post.id, 'comment_text': 'Nice post!'}
        
        response = self.client.post(self.comment_add_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['comments_count'], 1)
        self.assertTrue(Comment.objects.filter(text='Nice post!', user=self.user).exists())

    def test_load_more_posts(self):
        self.client.login(username='feeduser', password='password')
        
        for i in range(6):
            Post.objects.create(user=self.user, text=f"Pagination Post {i}")
            
        response = self.client.get(self.load_more_url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('html', data)
        self.assertTrue(len(data['html']) > 0)


class FeedsAPITests(TestCase):
    """
    Test suite untuk JSON API Endpoints (Mobile/Flutter).
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='apiuser', password='password')
        Profile.objects.create(user=self.user, display_name="API User")
        self.post = Post.objects.create(user=self.user, text="API Post")
        
        self.create_api_url = reverse('feeds_module:create_post_api')
        self.like_api_url = reverse('feeds_module:like_post_api')
        self.comment_api_url = reverse('feeds_module:add_comment_api')
        self.load_more_api_url = reverse('feeds_module:load_more_posts_api')

    def test_create_post_api(self):
        self.client.login(username='apiuser', password='password')
        data = {
            'text': 'JSON Post',
            'hashtags': 'api, json'
        }
        response = self.client.post(
            self.create_api_url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(text='JSON Post').exists())
        self.assertTrue(Hashtag.objects.filter(tag='api').exists())

    def test_like_post_api(self):
        self.client.login(username='apiuser', password='password')
        data = {'post_id': str(self.post.id)}
        
        response = self.client.post(
            self.like_api_url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['liked'])
        self.assertEqual(response.json()['likes_count'], 1)

    def test_add_comment_api(self):
        self.client.login(username='apiuser', password='password')
        data = {'post_id': str(self.post.id), 'comment_text': 'API Comment'}
        
        response = self.client.post(
            self.comment_api_url, 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(text='API Comment').exists())

    def test_load_more_posts_api(self):
        self.client.login(username='apiuser', password='password')
        response = self.client.get(self.load_more_api_url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('posts', data)
        self.assertGreaterEqual(len(data['posts']), 1)
        self.assertEqual(data['posts'][0]['text'], 'API Post')