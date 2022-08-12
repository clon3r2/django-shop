from django.urls import path
from .views import CartView, CartList, CartDetails, CartItemDelete, Payment, OffCodeCheck
app_name = 'order'

urlpatterns = [
    path('cart_details/' , CartDetails.as_view(), name='cart-details'),
    path('get_cart/' , CartList.as_view(), name='cart-list'),
    path('delete_cart_item/<int:product_id>' , CartItemDelete.as_view(), name='item-delete'),
    path('offcode_check', OffCodeCheck.as_view(), name='offcode-check'),
    path('add_to_cart/<int:product_id>/<int:quantity>', CartView.as_view(), name='add-to-cart'),
    path('payment/', Payment.as_view(), name='payment')
]