from decimal import Decimal
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class CartTests(APITestCase):
    fixtures = ['products.json', 'users.json']

    @classmethod
    def setUpClass(cls):
        super(CartTests, cls).setUpClass()
        cls.url = reverse('cart-detail')
        cls.user = User.objects.get_by_natural_key('admin')

    def test_cart_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_add_invalid_product(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'product': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Product does not exist')

    def test_cart_add_valid_product(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'product': 1, 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'product': 1,
            'quantity': 2,
            'unit_price': "350.00",
            'total_price': "700.00",
        })
        self._check_cart([response.json()])

    def test_cart_update_invalid_product(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'product': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Product does not exist')

    def test_cart_update_valid_product(self):
        self.client.force_authenticate(user=self.user)
        product = {'product': 2, 'quantity': 2}
        # Add a product into cart
        post_response = self.client.post(self.url, product)
        self._check_cart([post_response.json()])
        # Update the product quantity
        product['quantity'] = 3
        put_response = self.client.put(self.url, product)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.data, {
            'product': 2,
            'quantity': 3,
            'unit_price': "750.00",
            'total_price': "2250.00",
        })
        self._check_cart([put_response.json()])

    def test_cart_remove_product_required(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Product is required')

    def test_cart_remove_invalid_product(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, {'product': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Product does not exist')

    def test_cart_remove_valid_product(self):
        self.client.force_authenticate(user=self.user)
        # Add a product into cart
        response = self.client.post(self.url, {'product': 2, 'quantity': 2})
        self._check_cart([response.json()])
        # Remove above product from cart
        response = self.client.delete(self.url, {'product': 2})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._check_cart([])

    def _check_cart(self, products):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = response.json()
        total_price = sum([Decimal(p['total_price']) for p in products])
        self.assertAlmostEquals(total_price, Decimal(cart['total_price']))
