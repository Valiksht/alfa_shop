from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.decorators import action

from .models import MainCategiry, LastCategiry, Prodact, ShopBasket
from .serializers import (
    MainCategirySerializer,
    LastCategirySerializer,
    ProdactSerializer,
    ShopBasketSerializer
)
from .permissions import AdminOrReadOnly


class MainCategiryViewSet(viewsets.ModelViewSet):
    """ViewSet главной категории"""

    queryset = MainCategiry.objects.all().order_by('id')
    serializer_class = MainCategirySerializer
    permission_classes = (AdminOrReadOnly,)


class LastCategiryViewSet(viewsets.ModelViewSet):
    """ViewSet подкатегории"""

    queryset = LastCategiry.objects.all().order_by('id')
    serializer_class = LastCategirySerializer
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return LastCategiry.objects.filter(
            main_categiry__id=category_id
        ).order_by('id')

    def perform_create(self, serializer):
        category_id = self.kwargs.get('category_id')
        main_categiry = MainCategiry.objects.get(id=category_id)
        serializer.save(main_categiry=main_categiry)
        return super().perform_create(serializer)


class AllProdactViewSet(viewsets.ModelViewSet):
    """ViewSet всех продуктов"""

    queryset = Prodact.objects.all()
    serializer_class = ProdactSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProdactViewSet(viewsets.ModelViewSet):
    """ViewSet продуктов одной категории"""

    queryset = Prodact.objects.all()
    serializer_class = ProdactSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        lcategory_id = self.kwargs.get('lcategory_id')
        return Prodact.objects.filter(category=lcategory_id).order_by('id')

    def perform_create(self, serializer):
        lcategory_id = self.kwargs.get('lcategory_id')
        lcategory = LastCategiry.objects.get(id=lcategory_id)
        serializer.save(category=lcategory)
        return super().perform_create(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.images.all().delete()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shop_basket',
        permission_classes=(IsAuthenticated,)
    )
    def add_to_basket(self, request, *args, **kwargs):
        product = get_object_or_404(Prodact, pk=kwargs.get('pk'))
        print(product)
        user = self.request.user
        product_basket = ShopBasket.objects.filter(
            user=user, product=product).first()
        if request.method == 'POST':
            if product_basket:
                print(product_basket.value)
                product_basket.value += 1
                product_basket.save()
            else:
                ShopBasket.objects.create(user=user, product=product, value=1)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if product_basket.value > 1:
                product_basket.value -= 1
                product_basket.save()
            else:
                product_basket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return


class ShopBasketViewSet(viewsets.ModelViewSet):
    """ViewSet корзины"""

    queryset = ShopBasket.objects.all()
    serializer_class = ShopBasketSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_value = queryset.aggregate(total_value=Sum('value'))
        total_price = queryset.aggregate(total_price=Sum('product__price'))
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'items': serializer.data,
            'total_value': total_value['total_value'],
            'total_price': total_price['total_price']
        })

    @action(
        detail=False,
        methods=['delete'],
        url_path='delete_basket',
        permission_classes=(IsAuthenticated,)
    )
    def delete_basket(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
