from decimal import Decimal
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import ProductCreateSerializer
from collections import defaultdict


class ProductCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer



class ProductBulkCreateView(APIView):
    def post(self, request):
        items = request.data if isinstance(request.data, list) else []
        created_products, errors = [], []

        for idx, item in enumerate(items):
            ser = ProductCreateSerializer(data=item)
            if ser.is_valid():
                product = ser.save()
                created_products.append(product)
            else:
                errors.append({"index": idx, "errors": ser.errors})

        # Group products by categories (ManyToMany support)
        grouped = defaultdict(lambda: {"id": None, "name": "", "products": []})

        for product in created_products:
            for category in product.categories.all():
                if grouped[category.id]["id"] is None:
                    grouped[category.id]["id"] = category.id
                    grouped[category.id]["name"] = category.name
                grouped[category.id]["products"].append({
                    "id": product.id,
                    "name": product.name,
                })

        response_data = {
            "categories": list(grouped.values()),
            "errors": errors,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class CategoryAveragePrice(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cat = get_object_or_404(Category, pk=pk)
        cats = cat.get_descendants(include_self=True)
        qs = Product.objects.filter(categories__in=cats).distinct()
        avg = qs.aggregate(avg_price=Avg('price'))['avg_price'] or Decimal('0')
        avg = avg.quantize(Decimal("0.00"))
        return Response({"category": cat.name, "average_price": str(avg)})
