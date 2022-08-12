from django.contrib import admin
from .models import Coupon, Order, CartItem
# Register your models here.


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'value', 'type', 'max_price', 'valid_from', 'valid_to', 'is_active']
    fields = ['code', 'value', 'type', 'max_price', 'valid_from', 'valid_to']
    search_fields = ('code',)
    list_filter = ['last_updated']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'final_price', 'total_price']
    fields = ['customer', 'address', 'coupon']
    search_fields = ('customer', 'address')
    list_filter = ['last_updated']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'final_price']
    fields = ['product', 'quantity', 'cart']
    search_fields = ('product', )
    list_filter = ['last_updated']
