from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication
from .serializers import UserSerializer, AddressSerializer, CustomerSerializer, CartItemSerializer, OrderSerializer
from apps.customer.models import Address, Customer
from apps.core.models import User
from .permissions import IsOwnerPermission, IsSuperUserPermission, IsOwnerCartItemPermission
import django_filters.rest_framework
from rest_framework import filters
from apps.order.models import CartItem, Order
from django.http import JsonResponse


# -------User Detail/List------------------

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserPermission]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerPermission]


# -------Addresss Detail/List------------------

class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerPermission]

    def get_queryset(self):
        print(self.request.user)
        return Address.objects.filter(customer__user=self.request.user)


class AddressDetailView(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerPermission]


# -------Customer Detail/List------------------

class CustomerDetailView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id', 'user__phone', 'user__email']


# -------CartItem Detail/List------------------
class CartItemListView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()

    def post(self, request, *args, **kwargs):
        serializer_object = CartItemSerializer(data=request.data)
        serializer_object.is_valid(raise_exception=True)

        order_id = serializer_object.validated_data['order'].id
        product_id = serializer_object.validated_data['product'].id
        items = CartItem.objects.filter(order_id=order_id, product_id=product_id)
        if items.exists():
            old_item = items.first()
            old_item.quantity += int(serializer_object.validated_data['quantity'])
            old_item.save()
        else:
            serializer_object.save()
        return JsonResponse({'msg': 'ok'})


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = [IsOwnerCartItemPermission, permissions.IsAuthenticated]

    def delete(self, request, pk):
        cart_item = CartItem.objects.get(product_id=pk)
        cart_item.delete()
        return JsonResponse({'msg': 'ok'})


# -------Cart Detail/List------------------
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerCartItemPermission]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
