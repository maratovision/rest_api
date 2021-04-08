from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class MealTest(APITestCase):

    def setUp(self):
        self.meal_url = reverse('meal')

    def test_meal_get(self):
        self.response = self.client.get(self.meal_url)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
