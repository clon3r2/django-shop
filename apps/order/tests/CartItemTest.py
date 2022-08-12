from django.test import TestCase
from apps.product.models import Product, Discount
from apps.order.models import Cart, CartItem
# Create your tests here.


class CartItemTest(TestCase):
    def setUp(self) -> None:
        self.discount1 = Discount.objects.create(value=20, type='percent')
        self.discount2 = Discount.objects.create(value=50, type='percent')
        self.discount3 = Discount.objects.create(value=1500, type='price')
        self.product1 = Product.objects.create(name='product1', price=2000, slug='some-test-product1')
        self.product2 = Product.objects.create(name='product2', price=4000, slug='some-test-product2')
        self.product3 = Product.objects.create(name='product3', price=50000, slug='some-test-product3', discount=self.discount2)
        self.product4 = Product.objects.create(name='product4', price=4500, slug='some-test-product4', discount=self.discount3)
        self.cart_item1 = CartItem.objects.create(product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(product=self.product2, quantity=5)
        self.cart_item3 = CartItem.objects.create(product=self.product3, quantity=1)
        self.cart_item4 = CartItem.objects.create(product=self.product4, quantity=2)

    def test1_final_price(self):
        self.assertEqual(self.cart_item1.final_price, 4000)
        self.assertEqual(self.cart_item2.final_price, 20000)
        self.assertEqual(self.cart_item3.final_price, 25000)
        self.assertEqual(self.cart_item4.final_price, 6000)