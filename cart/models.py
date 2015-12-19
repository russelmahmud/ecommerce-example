from __future__ import unicode_literals

from decimal import Decimal
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from product.models import Product


class Cart(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    checked_out = models.BooleanField(default=False)

    def __iter__(self):
        """
        Allow the cart to be iterated giving access to the cart's items,
        ensuring the items are only retrieved once and cached.
        """
        if not hasattr(self, "_cached_items"):
            self._cached_items = self.items.all()
        return iter(self._cached_items)

    def add_item(self, product_pk, quantity):
        """
        Increase quantity of existing item, otherwise create
        new.
        """
        if not self.pk:
            self.save()

        kwargs = {'product_id': product_pk}
        item, created = self.items.get_or_create(**kwargs)

        if created:
            item.unit_price = item.product.unit_price

        item.quantity += quantity
        item.save()
        return item

    def has_items(self):
        return len(list(self)) > 0

    def total_quantity(self):
        return sum([item.quantity for item in self])

    def total_price(self):
        return sum([item.total_price for item in self])


@python_2_unicode_compatible
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items')
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=10)
    total_price = models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart #" + str(self.cart.pk) + " - " + str(self.product)

    def save(self, *args, **kwargs):
        """
        Set the total price based on the given quantity. If the
        quantity is zero, which may occur via the cart page, just
        delete it.
        """
        self.total_price = self.unit_price * self.quantity
        super(CartItem, self).save(*args, **kwargs)

    def to_json(self):
        return {
            'product': self.product.id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_price': self.total_price
        }
