import base64
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class CustomerTests(APITestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super(CustomerTests, cls).setUpClass()
        cls.url = reverse('authenticate')

    def test_auth_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_auth_login_failure(self):
        auth_password = base64.encodestring('admin:wrong').strip()
        self.client.credentials(HTTP_AUTHORIZATION='Basic {}'.format(auth_password))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_login_success(self):
        auth_password = base64.encodestring('admin:adminadmin').strip()
        self.client.credentials(HTTP_AUTHORIZATION='Basic {}'.format(auth_password))
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
