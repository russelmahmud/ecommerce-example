from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit_price', )


admin.site.register(Product, ProductAdmin)