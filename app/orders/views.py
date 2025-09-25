from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderCreateSerializer


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

