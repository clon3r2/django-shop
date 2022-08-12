from django.db import models
from apps.core.models import BaseDiscount, BaseModel
from apps.customer.models import Customer, Address
from apps.product.models import Product


class Coupon(BaseDiscount):
    code = models.CharField(max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        if self.type == 'percent':
            return f'{self.code}| {self.value}%'
        return f'{self.code}| {self.value}$'


class CartItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Item')
    quantity = models.IntegerField(default=1, verbose_name='Quantity')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    final_price = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def calc_final_price(self):
        """
        Calculate and Return the Final Price of an order item
        :param: instance
        :return final_price:
        """
        self.final_price = (self.product.price - self.product.discount.profit_value(self.product.price)) * self.quantity if self.product.discount else self.product.price * self.quantity

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
            sets final price automatically before saving the model object
        """
        self.calc_final_price()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.product.name}: {self.quantity}x'


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                    verbose_name='Customer', related_name='orders',
                                    null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    final_price = models.IntegerField(default=0, null=True, blank=True)
    total_price = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def calc_total_price(self):
        """
            Calculate and return total_price of Cart
            :param: self
            :return total_price:
        """
        self.total_price = sum([x.final_price for x in self.items.all()])

    def calc_final_price(self):
        """
            Calculate and return final_price of Cart (with Coupon)
            :param: self
            :return final_price:
        """
        self.final_price = (self.total_price - self.coupon.profit_value(self.final_price)) if self.coupon else self.total_price

    def close_order(self):
        self.is_active = False

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
            sets final and total price automatically before saving the model object
        """
        self.calc_total_price()
        self.calc_final_price()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.customer} - {self.final_price}'
