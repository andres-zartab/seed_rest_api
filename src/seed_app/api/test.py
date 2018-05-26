from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

from rest_framework_jwt.settings import api_settings

from django.contrib.auth import get_user_model

from seed_app.models import Seed

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class SeedTestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='420', email='420@420.com')
        user_obj.set_password('420024')
        user_obj.save()
        seed = Seed.objects.create(
            user=user_obj, 
            title='Pot Brownies', 
            content='Ganjhetas'
            )
    
    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1) 
    
    def test_single_seed(self):
        seed_count = Seed.objects.count()
        self.assertEqual(seed_count, 1) 

    def test_get_list(self):
        #Test the GET list
        data = {}
        uri = api_reverse('api-seed_app:seed-listcreate')
        response = self.client.get(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
    
    def test_post_item(self):
        #Test the POST 
        data = {'title': 'Shrooms', 'content': 'Amanita-Muscaria'}
        uri = api_reverse('api-seed_app:seed-listcreate')
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_item(self):
        #Test the GET list
        seed = Seed.objects.first()
        data = {}
        uri = seed.get_api_uri()
        response = self.client.get(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
    
    def test_update_item(self):
        #Test the POST 
        seed = Seed.objects.first()
        uri = seed.get_api_uri()
        data = {'title': 'Shrooms', 'content': 'Amanita-Muscaria'}
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        #Test the POST 
        seed = Seed.objects.first()
        uri = seed.get_api_uri()
        data = {'title': 'Shrooms', 'content': 'Amanita-Muscaria'}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_user(self):
        #Test the POST 
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {'title': 'Shrooms', 'content': 'Amanita-Muscaria'}
        uri = api_reverse('api-seed_app:seed-listcreate')
        response = self.client.post(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        #Test the POST 
        owner = User.objects.create(username='422')
        seed = Seed.objects.create(
            user=owner, 
            title='Galactic Spaguetti', 
            content='Weed Butter'
            )
        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        uri = seed.get_api_uri()
        data = {'title': 'Shrooms', 'content': 'Amanita-Muscaria'}
        response = self.client.put(uri, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_and_update(self):
        data = {
            'username': '420',
            'password': '420024'
        }
        uri = api_reverse('api-login')
        response = self.client.post(uri, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            seed = Seed.objects.first()
            uri = seed.get_api_uri()
            data = {'title': 'Shrooms', 'content': 'Amanita-Muscaria'}
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            response = self.client.put(uri, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)


