from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .cart import Cart, ItemDoesNotExist
from .serializers import CartItemSerializer, CartSerializer


class CartView(APIView):
    """
    API endpoint that allows add, update or remove product from cart.
    """
    authentication_classes = (BasicAuthentication, SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        cart = Cart(request)
        return Response(CartSerializer(cart.to_dict()).data)

    def post(self, request):
        cart = Cart(request)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                item = cart.add(serializer.data['product'], serializer.data['quantity'])
                serializer = CartItemSerializer(item.to_json())
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ItemDoesNotExist:
                return Response({'message': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        cart = Cart(request)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                item = cart.update(serializer.data['product'], serializer.data['quantity'])
                serializer = CartItemSerializer(item.to_json())
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ItemDoesNotExist:
                return Response({'message': 'Product does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = Cart(request)
        try:
            cart.remove(request.data['product'])
        except KeyError:
            return Response({'message': 'Product is required'},  status=status.HTTP_400_BAD_REQUEST)
        except ItemDoesNotExist:
            return Response({'message': 'Product does not exist'},  status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
