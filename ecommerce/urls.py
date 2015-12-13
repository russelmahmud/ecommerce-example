from django.conf.urls import url, include
from django.contrib import admin

from account.views import AuthView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/$', AuthView.as_view(), name='authenticate'),
    url(r'^api/v1/customers/', include('account.urls')),
    url(r'^api/v1/products/', include('product.urls')),
    url(r'^api/v1/cart/', include('cart.urls'))
]
