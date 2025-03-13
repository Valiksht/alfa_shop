from django.urls import include, path
from rest_framework import routers

from .views import (
    MainCategiryViewSet,
    LastCategiryViewSet,
    ProdactViewSet,
    AllProdactViewSet,
    ShopBasketViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('prodacts', AllProdactViewSet, basename='prodacts')
router.register('mcateg', MainCategiryViewSet, basename='mcategories')
router.register(
    r'mcateg/(?P<category_id>\d+)/lcateg/(?P<lcategory_id>\d+)/prodacts',
    ProdactViewSet,
    basename='prodacts'
)
router.register(
    r'mcateg/(?P<category_id>\d+)/lcateg',
    LastCategiryViewSet,
    basename='lcategories'
)
router.register('shopbasket', ShopBasketViewSet, basename='prodacts')

urlpatterns = [
    path('', include(router.urls)),
]
