from django.db import models
from apps.core.models import BaseModel
from apps.customer.models import Address
from apps.core.models import BaseDiscount


class Category(BaseModel):
    """
        Category Model has Self Relation
    """
    name = models.CharField(max_length=100)
    thumbnail = models.FileField(default='Default-Images/default_category.png', upload_to='categories/')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'


class Provider(BaseModel):
    """
        Provider Companies Bring Product lines of different brands
    """
    name = models.CharField(max_length=100, verbose_name='Company Name')
    description = models.TextField(max_length=100, verbose_name='Company Details', null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'


class Brand(BaseModel):
    """
        Product's original brands
    """
    name = models.CharField(max_length=100, verbose_name='Brand Name')
    country = models.CharField(max_length=100, verbose_name='Brand Country')
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, verbose_name='Brand Provider',
                                 null=True, blank=True)
    thumbnail = models.FileField(default='Default-Images/default_brand.png', upload_to='brands/')
    description = models.TextField(null=True, blank=True, verbose_name='Brand Details')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} from {self.provider}'


class Discount(BaseDiscount):
    """
        Discount model for Products
    """
    expire_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.type == 'percent':
            return f'{self.value}%'
        return f'{self.value}$'

class ProductImage(BaseModel):
    pic = models.FileField(default='Default-Images/product_default.jpg', upload_to='Products/', verbose_name='Product Images', blank=True, null=True)
    is_main = models.BooleanField(verbose_name='Is Main Image', default=False, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images',null=True, blank=True)

class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name='English name')
    fa_name = models.CharField(max_length=100, verbose_name='Farsi name', null=True, blank=True )
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    slug = models.SlugField(null=True, blank=True)
    price = models.IntegerField(verbose_name='Price')
    category = models.ForeignKey(Category, verbose_name='Category',
                                 related_name='products', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Brand',
                              related_name='products')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Discount', related_name='products', default=None)

    @property
    def final_price(self):
        return self.price - self.discount.profit_value(self.price) if self.discount else self.price
        
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} {self.price}'

