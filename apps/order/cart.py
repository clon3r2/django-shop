from apps.product.models import Product
from apps.order.models import Order, CartItem
CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID, None)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save()
    
    def add(self, product: Product, quantity):
        product_id = str(product.id)

        if product_id not in self.cart.keys():
            
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.final_price),
                'name': product.fa_name,
                'id': product.id,
                'image': product.images.first().pic.url
                }
        self.cart[product_id]['quantity'] += quantity
        self.save()
 
    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def save(self):
        self.session.modified = True
    
    def get_total_price(self):
        return sum(int(item['price'])* item['quantity'] for item in self.cart.values())  

    def clear(self):
        del self.session[CART_SESSION_ID]

    def session_merge_order(self, open_order: Order):
        """
        _summary_ : this functino merges open cart of a customer with cart items in session

        params:  open_order (Order): open order of a logged in customer
        """
        order_items = open_order.items.all() # all old items in open order of customer

        if order_items.exists():
            for i in order_items:
                if not str(i.product.id) in self.cart.keys(): # item in open order is not in session cart
                    self.add(i.product, i.quantity)
                else: # item in order is already in sessoin
                    new_quantity = int(self.cart[str(i.product.id)]['quantity'])
                    i.quantity = new_quantity
                    i.save()
        for i in self.cart.keys():
            if not int(i) in order_items.values_list('product_id', flat=True): # item in session cart is not in user open order
                CartItem.objects.create(product=Product.objects.get(id=int(i)),
                                        quantity=int(self.cart[i]['quantity']),
                                        order=open_order)
            
        





