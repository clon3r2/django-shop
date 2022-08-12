from .cart import Cart
from apps.order.models import Order
from apps.customer.models import Customer

def cart(request):
    return {'cart': Cart(request)}

def open_order(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        open_order, created = Order.objects.get_or_create(customer=customer, is_active=True)
        return {'open_order': open_order.id}
    return {'open_order': None}
