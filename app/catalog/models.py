from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name=models.CharField(max_length=120)
    parent=TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    class MPTTMeta:
        order_insertion_by=['name']
    class Meta:
        unique_together=("name","parent")

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=160)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    categories=models.ManyToManyField(Category, related_name='products')
    
    def __str__(self):
        return self.name
