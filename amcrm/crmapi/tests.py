from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status

# Create your tests here.

class UserTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword', is_staff=True)
        self.token = self.client.post(reverse('api_token_auth'), {'username':'testuser', 'password':'testpassword'}).data['token']
        self.customclient = APIClient()
        self.customclient.credentials(HTTP_AUTHORIZATION='Token '+self.token)

        self.create_url = reverse('api_user')

    def test_create_user(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'is_staff': False
        }

        response = self.customclient.post(self.create_url, data)

        # Two users in db
        self.assertEqual(User.objects.count(), 2)
        # 201 code return
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Return username and email
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo'*30,
            'email': 'foobarbaz@example.com',
            'password': 'foobar',
            'is_staff': False
        }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobar',
                'is_staff': False
                }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser',
                'is_staff': False
                }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_admin(self):
        data = {
                'username': 'adminuser',
                'email': 'adminuser@example.com',
                'password': 'adminuser',
                'is_staff': True
                }

        response = self.customclient.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['is_staff'])

#class CustomerTest(APITestCase):
#    def test_create_customer(self):

