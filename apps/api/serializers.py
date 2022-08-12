from rest_framework import serializers
from apps.customer.models import Address
from apps.core.models import User
from apps.customer.models import Customer
from apps.order.models import Order, CartItem


class AddressSerializer(serializers.ModelSerializer):
    customer = serializers.HyperlinkedRelatedField(read_only=True, view_name='api:customer-detail')  # __str__

    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', 'product', 'order']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'address', 'coupon', 'items']
