from django.urls import path
from .views import index, CategoryDetail, ProductDetail, BrandList, BrandDetail, ProductList
app_name = 'product'

urlpatterns = [
    path('', index, name='home'),
    path('categories/<int:category_id>', CategoryDetail.as_view(), name='category-detail'),
    path('brands/', BrandList.as_view(), name='brand-list'),
    path('brands/<int:brand_id>', BrandDetail.as_view(), name='brand-detail'),
    path('products/<int:product_id>', ProductDetail.as_view(), name='product-detail'),
]