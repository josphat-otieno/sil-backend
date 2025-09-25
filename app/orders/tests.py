from django.urls import reverse
from accounts.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Customer, Order, OrderItem
from catalog.models import Category


class OrderCreationTests(APITestCase):
    def setUp(self):
        # Customer
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )

        # Force authenticate for test client
        self.client.force_authenticate(user=self.user)

        self.customer = Customer.objects.create(
           user=self.user, phone="0712345678", email="john@example.com"
        )

        # Category tree
        self.category = Category.objects.create(name="Electronics")

        # Products with categories
        self.product1 = Product.objects.create(
            name="Laptop",
            price=1000
        )
        self.product1.categories.add(self.category)

        self.product2 = Product.objects.create(
            name="Mouse",
            price=50
        )
        self.product2.categories.add(self.category)

        self.url = reverse("order-create")  # Ensure your view has this name

    def test_create_order_with_items(self):
        """
        Ensure an order can be created with valid items.
        """
        data = {
            "customer": self.customer.id,
            "items": [
                {"product": self.product1.id, "quantity": 1},
                {"product": self.product2.id, "quantity": 2},
            ],
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.total, 1000 + 2 * 50)  # Laptop + 2 Mice

        # Verify items created
        self.assertEqual(OrderItem.objects.filter(order=order).count(), 2)

    def test_create_order_without_items(self):
        """
        Ensure an order cannot be created without items.
        """
        data = {
            "customer": self.customer.id,
            "items": [],
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("items", response.data)
