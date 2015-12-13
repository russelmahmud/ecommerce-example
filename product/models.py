from __future__ import unicode_literals

from decimal import Decimal
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name
