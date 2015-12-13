from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.StackedInline):
    model = CartItem
    can_delete = False


class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline, )


admin.site.register(Cart, CartAdmin)
