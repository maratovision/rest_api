from .models import Order
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class OrderTest(APITestCase):

    def setUp(self):
        self.order_url = reverse('order')

    def test_order_create(self):
        data = {
                "id": 68,
                "total_price": 150,
                "table": 1,
                "status": "in process",
                "date_created": "2021-04-06T23:32:11.716683+06:00",
                "user_profile": 2,
                "total_sum": 150,
                "worker": 2,
                "MTO": [
                    {
                        "id": 29,
                        "meal": 1,
                        "quantity": 1
                    }
                ]
            }
        self.response = self.client.post(self.order_url,data)
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
