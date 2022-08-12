from django.contrib import admin
from .models import Customer, Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']
    fields = ['user', 'gender', 'image']
    list_filter = ('last_updated', )

admin.site.register(Address)