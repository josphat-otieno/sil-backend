from django.db import models
from accounts.models import Customer
from catalog.models import Product

class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    total=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Order #{self.pk} - {self.customer}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10, decimal_places=2)

