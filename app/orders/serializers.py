from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem, Product, Customer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]  # price will be taken from product


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "items", "total", "created_at"]
        read_only_fields = ["id", "total", "created_at"]

    def validate_items(self, value):
        """Ensure at least one order item is provided."""
        if not value:
            raise serializers.ValidationError("An order must have at least one item.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")

        order = Order.objects.create(**validated_data)

        total = 0
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data.get("quantity", 1)
            price = product.price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )
            total += quantity * price

        
        order.total = total
        order.save()


        return order
