from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
UserAdmin.list_display =('phone', 'email', 'first_name', 'last_name', 'is_staff')
UserAdmin.fieldsets[0][1]['fields'] = ('phone', 'password')
UserAdmin.add_fieldsets[0][1]['fields'] = ('phone', 'password1', 'password2')
admin.site.register(User, UserAdmin)
