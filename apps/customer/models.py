from django.utils.translation import gettext as _
from django.db import models
from apps.core.models import User
from apps.core.models import BaseModel
import os


class Address(BaseModel):
    """
        Customer's Addresses (a customer can have multiple addresses)
    """
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    address = models.TextField()
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name='userAddress')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.customer} : {self.city}-{self.address}'


def get_upload_path(instance, filename):
    return os.path.join(
        instance.id,
        instance.first_name, instance.last_name,
        filename
        )    


class Customer(BaseModel):
    
    gender_choices = (
        ('male', 'مذکر'),
        ('female', 'مونث')
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'), default=None, blank=True, null=True)
    image = models.FileField(default='Default-Images/default_user.png', upload_to='user_profiles/', blank=True, null=True, verbose_name='Profile Image')
    gender = models.CharField(choices=gender_choices, null=True, blank=True, verbose_name='Gender', max_length=10)

    class Meta:
        ordering = ['-created']
        permissions = [
            ('view_profile', 'Can view the customer profile page'),
            ('edit_user_info', 'Can edit the customer User info')
        ]

    def __str__(self):
        return f'{self.user}'
