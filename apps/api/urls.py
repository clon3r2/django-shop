# Shop Url configs
from django.urls import path, include
from .views import UserListView, AddressDetailView, AddressListView, UserDetailView, CustomerDetailView, CustomerListView, CartItemListView, CartItemDetailView, OrderListView, OrderDetailView

app_name = 'api'

urlpatterns = [
    path('user-list', UserListView.as_view(), name='user-list'),
    path('address-list', AddressListView.as_view(), name='address-list'),
    path('user-detail/<pk>', UserDetailView.as_view(), name='user-detail'),
    path('address-detail/<pk>', AddressDetailView.as_view(), name='address-detail'),
    path('customer-detail/<pk>', CustomerDetailView.as_view(), name='customer-detail'),
    path('customer-list/', CustomerListView.as_view(), name='customer-list'),
    path('cartitem-detail/<pk>', CartItemDetailView.as_view(), name='cartitem-detail'),
    path('cartitem-list/', CartItemListView.as_view(), name='cartitem-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('order-detail/<pk>', OrderDetailView.as_view(), name='order-detail'),
]