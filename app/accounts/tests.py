from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer
from django.urls import reverse


class UpdateCustomerPhoneAPITest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.customer = Customer.objects.create(user=self.user, email="test@example.com")

        # Force authenticate for test client
        self.client.force_authenticate(user=self.user)

        self.url = reverse("update-phone") 
    def test_update_phone_success(self):
        data = {"phone": "254712345678"}
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "254712345678")

    def test_update_phone_invalid_format(self):
        data = {"phone": "12345"}
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)

        