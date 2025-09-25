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
        categories = validated_data.pop('category_paths')
        product = Product.objects.create(**validated_data)
        parent = None
        for name in categories:   # now it's just a flat list of strings
            parent, _ = Category.objects.get_or_create(name=name, parent=parent)

        product.categories.add(parent)
        return product
