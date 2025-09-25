from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal

from .models import Product, Category


class ProductCategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_bulk_create_products_with_categories(self):
        """Test bulk product creation with nested categories"""
        payload = [
            {
                "name": "Mango",
                "price": "120.50",
                "categories": [["Fruits", "Tropical"]],
            },
            {
                "name": "Apple",
                "price": "80.00",
                "categories": [["Fruits", "Temperate"]],
            },
        ]

        url = reverse("product-bulk-create") 
        res = self.client.post(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Category.objects.count(), 3) 

    def test_average_price_for_category(self):
        """Test that average product price is calculated correctly"""
        fruits = Category.objects.create(name="Fruits")
        tropical = Category.objects.create(name="Tropical", parent=fruits)

        p1 = Product.objects.create(name="Mango", price=Decimal("100.00"))
        p2 = Product.objects.create(name="Banana", price=Decimal("200.00"))

        p1.categories.add(tropical)
        p2.categories.add(tropical)

        url = reverse("category-average-price", args=[fruits.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["average_price"], "150.00")

