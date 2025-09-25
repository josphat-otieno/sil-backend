from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer",  "created_at", "total")
    list_filter = ( "created_at",)
    search_fields = ("customer__email__icontains", "customer__phone__icontains", "id")
    ordering = ("-created_at",)



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    search_fields = ("order__id", "product__name__icontains")
    ordering = ("-id",)

