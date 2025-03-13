from django.db import models
from django.contrib.auth import get_user_model

from alfa_shop.constants import NAME_LEN, SLUG_LEN


class MainCategiry(models.Model):
    name = models.CharField(
        max_length=NAME_LEN, verbose_name='Название категории'
    )
    slug = models.SlugField(max_length=SLUG_LEN, verbose_name='Слаг категории')
    image = models.ImageField(
        upload_to='categiry', verbose_name='Изображение категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class LastCategiry(models.Model):
    name = models.CharField(
        max_length=NAME_LEN, verbose_name='Название подкатегории'
    )
    slug = models.SlugField(
        max_length=SLUG_LEN, verbose_name='Слаг подкатегории'
    )
    image = models.ImageField(
        upload_to='categiry', verbose_name='Изображение подкатегории'
    )
    main_categiry = models.ForeignKey(
        MainCategiry, on_delete=models.CASCADE, verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Prodact(models.Model):
    name = models.CharField(
        max_length=NAME_LEN, verbose_name='Название товара'
    )
    slug = models.SlugField(
        max_length=SLUG_LEN, verbose_name='Слаг товара'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена товара'
    )
    category = models.ForeignKey(
        LastCategiry, on_delete=models.CASCADE, verbose_name='Подкатегория'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProdactImage(models.Model):
    image = models.ImageField(
        upload_to='prodact', verbose_name='Изображение товара'
    )
    prodact = models.ForeignKey(
        Prodact, related_name='images',
        on_delete=models.CASCADE, verbose_name='Товар'
    )


class ShopBasket(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Prodact, on_delete=models.CASCADE, verbose_name='Товар'
    )
    value = models.IntegerField(verbose_name='Количество товара')

    class Meta:
        verbose_name = 'Корзина'
