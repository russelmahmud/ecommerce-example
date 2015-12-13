from rest_framework import serializers


class CartItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1)
    unit_price = serializers.DecimalField(10, 2, required=False)
    total_price = serializers.DecimalField(10, 2, required=False)


class CartSerializer(serializers.Serializer):
    checked_out = serializers.BooleanField(default=False)
    total_price = serializers.DecimalField(10, 2, required=False)
    items = CartItemSerializer(many=True, read_only=True)
