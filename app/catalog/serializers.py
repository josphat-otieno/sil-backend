from rest_framework import serializers
from .models import Category, Product

class CategoryPathField(serializers.ListField):
    child = serializers.CharField()

class ProductCreateSerializer(serializers.ModelSerializer):
    category_paths = CategoryPathField(write_only=True, required=True)
    class Meta:
        model = Product
        fields = ['id','name','price','category_paths']
    def create(self, validated_data):
        paths = validated_data.pop('category_paths')
        product = Product.objects.create(**validated_data)
        for path in paths:
            parent=None
            for name in path:
                parent,_=Category.objects.get_or_create(name=name, parent=parent)
            product.categories.add(parent)
        return product
