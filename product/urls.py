from django.conf.urls import url

from .views import ProductViewSet


product_list = ProductViewSet.as_view({'get': 'list'})
product_detail = ProductViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    url(r'^$', product_list, name='product-list'),
    url(r'^(?P<pk>[0-9]+)/$', product_detail, name='product-detail')
]
