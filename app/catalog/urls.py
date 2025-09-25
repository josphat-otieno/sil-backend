from django.urls import path
from .views import ProductCreateView, ProductBulkCreateView, CategoryAveragePrice
urlpatterns=[
    path('products/', ProductCreateView.as_view(), name='product-create'),
    path('products/bulk/', ProductBulkCreateView.as_view(), name='product-bulk'),
    path('categories/<int:pk>/average-price/', CategoryAveragePrice.as_view(), name='category-average'),
]
