from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class ProductTests(APITestCase):
    fixtures = ['products.json']

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = response.json()
        self.assertEqual(products['count'], 4)

    def test_product_detail(self):
        url = reverse('product-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = response.json()
        self.assertDictEqual(product, {
            "id": 1,
            "name": "iPad",
            "quantity": 5,
            "unit_price": "350.00"
        })
