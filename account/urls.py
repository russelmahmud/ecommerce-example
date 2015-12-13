from django.conf.urls import url

from .views import UserView

user_list = UserView.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update'
})

urlpatterns = [
    url(r'^$', user_list, name='user-list'),
    url(r'^(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
]
