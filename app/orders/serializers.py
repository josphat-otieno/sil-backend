from rest_framework import serializers
from decimal import Decimal
from accounts.models import Customer
from catalog.models import Product
from .models import Order, OrderItem

class OrderItemIn(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderOutItem(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product","quantity","price"]

class OrderOut(serializers.ModelSerializer):
    items = OrderOutItem(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id","customer","created_at","total","items"]

class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemIn(many=True)
    def create(self, validated_data):
        user = self.context["request"].user
        customer, _ = Customer.objects.get_or_create(user=user, defaults={"email": getattr(user,"email","") or "", "phone": ""})
        order = Order.objects.create(customer=customer)
        total = Decimal("0")
        for it in validated_data["items"]:
            p = Product.objects.get(pk=it["product_id"])
            qty = it["quantity"]
            OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
            total += p.price * qty
        order.total = total
        order.save()
        from notifications.tasks import notify_order_placed
        notify_order_placed(order.id)
        return order
