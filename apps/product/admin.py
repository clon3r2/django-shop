from django.contrib import admin
from .models import Product, Category, Discount, Brand, Provider, ProductImage


# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['pic', 'product', 'is_main']
    extra = 3


class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name', 'fa_name', 'description', 'price']
    extra = 3


class BrandInline(admin.TabularInline):
    model = Brand
    fields = ['name', 'country', 'thumbnail', 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'fa_name', 'price']
    fields = ['name', 'fa_name', 'description', 'slug', 'category', 'price', 'brand', 'discount']
    search_fields = ('name',)
    list_filter = ['last_updated']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('description',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name', 'thumbnail', 'parent']
    search_fields = ('name',)
    inlines = [ProductInline]
    list_filter = ['last_updated']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['value', 'type', 'max_price', 'is_active']
    fields = ['value', 'type', 'max_price', 'expire_date', 'is_active']
    search_fields = ('value', 'type',)
    list_filter = ['last_updated']
    inlines = [ProductInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'provider']
    fields = ['name', 'country', 'provider', 'thumbnail', 'description']
    search_fields = ('name', 'provider', 'country')
    list_filter = ['last_updated']
    inlines = [ProductInline]


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    fields = ['name', 'description', 'address']
    search_fields = ('name',)
    list_filter = ['last_updated']
    inlines = [BrandInline]
