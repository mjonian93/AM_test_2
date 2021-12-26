from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Customer

# Create your tests here.

class UserTest(APITestCase):
    def setUp(self):
        self.test_user_admin = User.objects.create_user('testuseradmin', 'testadmin@example.com',
                                                        'testpasswordadmin', is_staff=True)
        self.token_admin = self.client.post(reverse('api_token_auth'), {'username': 'testuseradmin',
                                                                  'password': 'testpasswordadmin'}).data['token']
        self.customclient_admin = APIClient()
        self.customclient_admin.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin)

        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword', is_staff=False)
        self.token = self.client.post(reverse('api_token_auth'), {'username':'testuser',
                                                                  'password':'testpassword'}).data['token']
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

        response = self.customclient_admin.post(self.create_url, data)

        # Two users in db
        self.assertEqual(User.objects.count(), 3)
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

        response = self.customclient_admin.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobar',
                'is_staff': False
                }

        response = self.customclient_admin.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser',
                'is_staff': False
                }

        response = self.customclient_admin.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_admin(self):
        data = {
                'username': 'adminuser',
                'email': 'adminuser@example.com',
                'password': 'adminuser',
                'is_staff': True
                }

        response = self.customclient_admin.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['is_staff'])

    def test_modify_user_with_admin_token(self):
        data = {
            'username': 'adminuser',
            'email': 'adminuser@example.com',
            'password': 'adminuser',
            'is_staff': True
        }

        response = self.customclient_admin.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_update = {
            'email': 'modified_email@example.com'
        }
        response = self.customclient_admin.patch('http://127.0.0.1:8000/api/users/3', data_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data['data']
        self.assertEqual(response_data['email'], data_update['email'])

    def test_modify_user_without_admin_token(self):
        data = {
            'username': 'adminuser',
            'email': 'adminuser@example.com',
            'password': 'adminuser',
            'is_staff': True
        }

        response = self.customclient_admin.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_update = {
            'email': 'modified_email@example.com'
        }
        response = self.customclient.patch('http://127.0.0.1:8000/api/users/3', data_update)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CustomerTest(APITestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user('testuser1', 'testuser1@example.com', 'testpassword1', is_staff=False)
        self.token_user1 = self.client.post(reverse('api_token_auth'), {'username':'testuser1',
                                                                        'password':'testpassword1'}).data['token']
        self.customclient1 = APIClient()
        self.customclient1.credentials(HTTP_AUTHORIZATION='Token '+self.token_user1)

        self.test_user2 = User.objects.create_user('testuser2', 'testuser2@example.com', 'testpassword2', is_staff=False)
        self.token_user2 = self.client.post(reverse('api_token_auth'), {'username': 'testuser2',
                                                     'password': 'testpassword2'}).data['token']
        self.customclient2 = APIClient()
        self.customclient2.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2)

        self.create_url = reverse('api_customer')

    def test_create_customer(self):
        data = {
            'name': 'Chad',
            'surname': 'Smith'
        }

        response = self.customclient1.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, response.data['creator'])

    def test_create_customer_with_too_long_name(self):
        data = {
            'name': 'foo'*30,
            'surname': 'bar'
        }

        response = self.customclient1.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_customer_with_too_long_surname(self):
        data = {
            'name': 'foo',
            'surname': 'bar'*30
        }

        response = self.customclient1.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 0)

    def test_modify_customer_check_last_modifier(self):
        data = {
            'name': 'Chad',
            'surname': 'Smith'
        }
        response = self.customclient1.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_update = {
            'surname': 'Williams'
        }
        response = self.customclient2.patch('http://127.0.0.1:8000/api/customers/1', data_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data['data']
        self.assertEqual(2, response_data['last_modifier'])

    def test_upload_image(self):
        data = {
            'name': 'Chad',
            'surname': 'Smith'
        }
        response = self.customclient1.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_update = {
            "image": SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        }
        response = self.customclient1.patch('http://127.0.0.1:8000/api/customers/1', data_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data['data']
        self.assertTrue(response_data['image'])




