from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model

from postings.models import BlogPost
#automated
#new blank db
#NOTE: Manueally creating new token form JWT doc
#request.post(url, data, headers={'Authorization': 'JWT '+<token>})
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='420_test_user', email='420@420.com')
        user_obj.set_password('XX024')
        user_obj.save()
        #NOTE: User.objects.create(username='420_test_user', email='420@420.com') could be used and remove save()
        
        blog_post = BlogPost.objects.create(
            user=user_obj,
            title='Smoke Everyday',
            content = 'Weed, of course. 420!'
            )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_post_item(self):
        data = {'title': '422', 'content': 'Bongs and Blunt Braah'}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #print(response.data)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        data = {'title': '422', 'content': 'Bongs and Blunt Braah'}
        url = blog_post.get_api_url()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        print(blog_post.content)
        data = {'title': '422', 'content': 'Bongs and Blunt Braah'}
        url = blog_post.get_api_url()
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        #NOTE: everytime I pass a request thats related to my user I need to pass this token
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_post_item_with_user(self):
        data = {'title': '422', 'content': 'Bongs and Blunt Braah'}
        url = api_reverse('api-postings:post-listcreate')
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='422_test_user', email='422@422.com')
        
        blog_post = BlogPost.objects.create(
            user=owner,
            title='Smoke Everyday',
            content = 'Weed, of course. 420!'
            )
        user_obj    = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload     = payload_handler(user_obj)
        token_rsp   = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data = {'title': '422', 'content': 'Bongs and Blunt Braah'}
        url = blog_post.get_api_url()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_and_update(self):
        data = {
            'username': '420_test_user',
            'password': 'XX024'
        }
        
        url = api_reverse('api-login')
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #NOTE: This test works because of the setUp
        token = response.data.get('token')
        if token is not None:
            blog_post = BlogPost.objects.first()
            data = {'title': '422', 'content': 'Bongs and Blunt Braah'}
            url = blog_post.get_api_url()
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)