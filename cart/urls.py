from django.conf.urls import url

from .views import CartView

urlpatterns = [
    url(r'^$', CartView.as_view(), name='cart-detail'),
]
