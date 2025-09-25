from rest_framework import serializers
from .models import Category, Product

class CategoryPathField(serializers.ListField):
    child = serializers.CharField()

class ProductCreateSerializer(serializers.ModelSerializer):
    category_paths = CategoryPathField(write_only=True, required=True)
    class Meta:
        model = Product
        fields = ['id','name','price','categories']
    def create(self, validated_data):
        categories = validated_data.pop('categories')
        product = Product.objects.create(**validated_data)
        for category in categories:
            parent=None
            for name in category:
                parent,_=Category.objects.get_or_create(name=name, parent=parent)
            product.categories.add(parent)
        return product
