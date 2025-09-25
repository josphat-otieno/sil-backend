from rest_framework import generics
from .models import Order
from .serializers import OrderCreateSerializer, OrderOut

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOut
