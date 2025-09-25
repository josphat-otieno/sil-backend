from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Customer, Product, Order


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="John Doe", email="john@example.com")
        self.product1 = Product.objects.create(name="Laptop", price=Decimal("1000.00"))
        self.product2 = Product.objects.create(name="Mouse", price=Decimal("50.00"))

    def test_create_order_with_phone_number(self):
        url = reverse("order-create")
        data = {
            "customer": self.customer.id,
            "phone_number": "+254700000000",
            "items": [
                {"product": self.product1.id, "quantity": 1},
                {"product": self.product2.id, "quantity": 2},
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.phone_number, "+254700000000")
        self.assertEqual(order.total, Decimal("1100.00"))
        self.assertEqual(order.items.count(), 2)

    def test_order_without_items_fails(self):
        url = reverse("order-create")
        data = {
            "customer": self.customer.id,
            "phone_number": "+254711111111",
            "items": []
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Order must have at least one item.", str(response.data))

    def test_order_without_phone_number_fails(self):
        url = reverse("order-create")
        data = {
            "customer": self.customer.id,
            # phone_number missing
            "items": [
                {"product": self.product1.id, "quantity": 1},
            ]
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone_number", response.data)
