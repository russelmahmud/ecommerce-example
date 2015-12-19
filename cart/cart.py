from django.conf import settings
from django.db.models import F

from product.models import Product
from .models import CartItem, Cart as CartModel

CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', 'CART-ID')


class Cart(object):
    def __init__(self, request):
        cart_id = request.session.get(CART_SESSION_KEY)
        if cart_id:
            try:
                cart = CartModel.objects.get(id=cart_id, checked_out=False)
            except CartModel.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)

        self.cart = cart

    def __iter__(self):
        if not hasattr(self, "_cached_items"):
            self._cached_items = self.cart.items.all()

        for item in self._cached_items:
            yield item

    def __contains__(self, product_pk):
        """
        Checks if the given product is in the cart.
        """
        return product_pk in self.products

    def _get_product(self, product_pk):
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            raise ItemDoesNotExist

        return product

    @property
    def products(self):
        """
        The list of associated products.
        """
        return [item.product.pk for item in self.cart.items.all()]

    def new(self, request):
        cart = CartModel()
        cart.save()
        request.session[CART_SESSION_KEY] = cart.id
        return cart

    def add(self, product_pk, quantity):
        product = self._get_product(product_pk)
        try:
            item = CartItem.objects.get(cart=self.cart, product=product)
            item.unit_price = product.unit_price
            item.quantity = F('quantity') + quantity
            item.save()
        except CartItem.DoesNotExist:
            item = CartItem(cart=self.cart, product=product)
            item.unit_price = product.unit_price
            item.quantity = quantity
            item.save()

        return item

    def remove(self, product):
        try:
            item = CartItem.objects.get(cart=self.cart, product=product)
        except CartItem.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product_pk, quantity):
        product = self._get_product(product_pk)
        try:
            item = CartItem.objects.get(cart=self.cart, product=product)
        except CartItem.DoesNotExist:
            raise ItemDoesNotExist
        else:
            if quantity == 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()

        return item

    def count(self):
        result = 0
        for item in self.cart.items.all():
            result += item.quantity
        return result

    def summary(self):
        result = 0
        for item in self.cart.items.all():
            result += item.total_price
        return result

    def clear(self):
        for item in self.cart.items.all():
            item.delete()

    def to_dict(self):
        result = dict()
        result['total_price'] = self.summary()
        result['id'] = self.cart.id
        result['checked_out'] = self.cart.checked_out
        result['items'] = []
        for item in self:
            result['items'].append({
                'product': item.product.pk,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total_price': item.total_price
            })
        return result


class ItemDoesNotExist(Exception):
    pass
