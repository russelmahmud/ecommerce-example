from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class CustomerTests(APITestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super(CustomerTests, cls).setUpClass()
        cls.admin_user = User.objects.get_by_natural_key('admin')
        cls.normal_user = User.objects.get_by_natural_key('russel')

    def test_customers_list_for_unauthorized(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customers_list_for_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customers = response.json()
        self.assertEqual(customers['count'], 2)

    def test_customers_list_for_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customers = response.json()
        self.assertEqual(customers['count'], 1)
        self.assertEqual(customers['results'][0]['id'], 9)

    def test_customer_detail_unauthorized(self):
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_detail_invalid_id(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-detail', kwargs={'pk': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_detail_404_for_unauthorized_user(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('user-detail', kwargs={'pk': self.admin_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_detail_valid_id(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('user-detail', kwargs={'pk': self.normal_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.normal_user.pk)

    def test_customer_create(self):
        url = reverse('user-list')
        post_response = self.client.post(url, {
            'username': 'Test',
            'password': 'testtest',
            'email': 'test@example.com'
        })
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_response.json()['username'], 'Test')
        self.assertIsNotNone(post_response.json()['id'])
