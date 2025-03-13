import base64

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from .models import MainCategiry, LastCategiry, Prodact, ShopBasket, ProdactImage

User = get_user_model()

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class LastCategirySerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    main_categiry = serializers.PrimaryKeyRelatedField(queryset=MainCategiry.objects.all(), required=False)

    class Meta:
        model = LastCategiry
        fields = ['id', 'name', 'slug', 'image', 'main_categiry']
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.main_categiry:
            data['main_categiry'] = instance.main_categiry.name
        return data

class MainCategirySerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    last_categiry = serializers.SerializerMethodField()

    class Meta:
        model = MainCategiry
        fields = ['id', 'name', 'slug', 'image', 'last_categiry']
        read_only_fields = ['id', 'last_categiry']

    def get_last_categiry(self, obj):
        last_categiry = LastCategiry.objects.filter(main_categiry=obj)
        return LastCategirySerializer(last_categiry, many=True).data

class LastCategirySerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    main_categiry = serializers.PrimaryKeyRelatedField(queryset=MainCategiry.objects.all(), required=False)

    class Meta:
        model = LastCategiry
        fields = ['id', 'name', 'slug', 'image', 'main_categiry']
        read_only_fields = ['id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.main_categiry:
            data['main_categiry'] = instance.main_categiry.name
        return data

class ProdactImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = ProdactImage
        fields = ['image']


class ProdactSerializer(serializers.ModelSerializer):
    images = ProdactImageSerializer(many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=LastCategiry.objects.all(), required=False)
    main_category = serializers.SerializerMethodField()

    class Meta:
        model = Prodact
        fields = ['id', 'name', 'slug', 'images', 'category', 'price', 'main_category']
        read_only_fields = ['id', 'main_category', 'category']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.category:
            data['category'] = instance.category.name
        return data
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        prodact = Prodact.objects.create(**validated_data)
        for image_data in images_data:
            ProdactImage.objects.create(prodact=prodact, **image_data)
        return prodact
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        prodact = super().update(instance, validated_data)
        instance.images.all().delete()
        for image_data in images_data:
            ProdactImage.objects.create(prodact=prodact, **image_data)
        return prodact
    
    def get_main_category(self, obj):
        return obj.category.main_categiry.name

class ShopBasketSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Prodact.objects.all(), required=False)
    # value = serializers.SerializerMethodField()

    class Meta:
        model = ShopBasket
        fields = ['id', 'user', 'product', 'value']
        read_only_fields = ['id', 'value']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = ProdactSerializer(instance.product).data
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)    

