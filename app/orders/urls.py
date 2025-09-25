from django.urls import path
from .views import OrderCreateView, OrderDetailView
urlpatterns=[
    path('orders/', OrderCreateView.as_view(), name='order-create'),
]
