from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class RegisterTest(APITestCase):

    def setUp(self):
        self.register_url = reverse('create')
        User.objects.create(username='maksim777', password='123456')

    def test_user_create(self):
        data = {
                "username":"maksim",
                "email":"maximneveraa@gmail.com",
                "first_name":"maksim",
                "last_name":"surovkin",
                "password":"12345678",
                "confirm_password":"12345678"
            }
        self.response = self.client.post(self.register_url,data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_username_exist(self):
        data = {
            "username": "maksim777",
            "email": "maximneveraa@gmail.com",
            "first_name": "maksim",
            "last_name": "surovkin",
            "password": "12345678",
            "confirm_password": "12345678"
        }
        self.response = self.client.post(self.register_url,data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_len(self):
        data = {
            "username": "maskim777",
            "email": "maximneveraa@gmail.com",
            "first_name": "maksim",
            "last_name": "surovkin",
            "password": "123456",
            "confirm_password": "123456"
        }
        self.response = self.client.post(self.register_url, data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)