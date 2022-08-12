from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
import sweetify
from apps.customer.models import Address
from .cart import Cart
from apps.product.models import Product
from django.shortcuts import get_object_or_404
from apps.order.forms import AddressForm
from .models import Order, Coupon
from django.contrib.auth.mixins import LoginRequiredMixin


class CartView(View):

    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return super().setup(request, *args, **kwargs)

    def post(self, request, product_id, quantity):
        product = get_object_or_404(Product, pk=product_id)
        self.cart.add(product, quantity)
        return JsonResponse({'TotalItems': self.cart.__len__(), 'url': reverse('order:cart-list')}, safe=False)


class CartList(View):
    template_name = 'order/cart.html'

    def get(self, request):
        return render(request, self.template_name)


class CartDetails(LoginRequiredMixin, View):
    template_name = 'order/cart_detail.html'

    def get(self, request):
        return render(request, self.template_name, {'address_form': AddressForm(customer=request.user.customer)})


class CartItemDelete(View):

    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return super().setup(request, *args, **kwargs)

    def delete(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        self.cart.remove(product=product)
        return JsonResponse({'TotalItems': self.cart.__len__(), 'url': reverse('order:cart-list'),
                             'total_price': self.cart.get_total_price()}, safe=False)


class Payment(View):

    def setup(self, request, *args, **kwargs) -> None:
        self.cart = Cart(request)
        return super().setup(request, *args, **kwargs)

    def post(self, request):
        address = Address.objects.get(id=request.POST['address'])
        open_order = Order.objects.get(customer=request.user.customer, is_active=True)
        open_order.address = address

        open_order.deactivate()

        open_order.save()

        self.cart.clear()

        Order.objects.create(customer=request.user.customer)
        sweetify.toast(request, "Your Order Submitted Successfully.", icon="success", timer=1500)

        return redirect('product:home')


class OffCodeCheck(View):
    def setup(self, request, *args, **kwargs):
        offcode = request.POST.get('offCode')
        self.offcode = Coupon.objects.filter(code=offcode, is_active=True,
                                             valid_from__lte=timezone.now(),
                                             valid_to__gte=timezone.now())
        self.offcode = self.offcode.first() if self.offcode.exists() else None
        print(self.offcode)
        self.open_order = Order.objects.get(customer=request.user.customer, is_active=True)
        return super().setup(request, *args, **kwargs)

    def post(self, request):
        if not self.offcode:
            return JsonResponse({'msg': 'NotValid'}, safe=False)
        if self.open_order.coupon:
            self.open_order.coupon = None
            self.open_order.save()
            self.open_order.coupon = self.offcode
            self.open_order.save()
        else:
            self.open_order.coupon = self.offcode
            self.open_order.save()
        print(self.open_order.final_price)
        return JsonResponse({"msg": 'Success', "final_price": self.open_order.final_price}, safe=False)
