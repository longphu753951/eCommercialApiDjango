from django.db.models import Min
from rest_framework import serializers
from .models import Category, Product, ProductAttribute, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    image_outline = serializers.SerializerMethodField(source='image')
    image_solid = serializers.SerializerMethodField(source='image')

    def get_image_outline(self, obj):
        request = self.context['request']
        if obj.image_outline and not obj.image_outline.name.startswith('/static'):
            path = '/static/%s' % obj.image_outline.name

            return request.build_absolute_uri(path)

    def get_image_solid(self, obj):
        request = self.context['request']
        if obj.image_outline and not obj.image_solid.name.startswith('/static'):
            path = '/static/%s' % obj.image_solid.name

            return request.build_absolute_uri(path)

    class Meta:
        model = Category
        fields = ["id", "name", "image_outline", "image_solid"]


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context['request']
        if obj.image and not obj.image.name.startswith('/static'):
            path = '/static/%s' % obj.image.name

            return request.build_absolute_uri(path)

    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    productImage = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ["sku", "color", "hexColor", "sale_off", "on_stock", "price", "active", "product", "productImage"]


class ProductSerializer(serializers.ModelSerializer):
    productAttribute = serializers.SerializerMethodField('get_productAttribute')
    product = Product.objects

    def get_productAttribute(self, product):
        serializer_context = {'request': self.context.get('request')}
        source = product.productAttribute.annotate(Min('price')).order_by('price')[0]
        return ProductAttributeSerializer(instance=source, many=False, context=serializer_context).data

    class Meta:
        model = Product
        fields = ["id", "name", "rating", "description", "category", 'productAttribute']


class ProductDetailSerializer(serializers.ModelSerializer):
    productAttribute = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "rating", "description", "category", 'productAttribute']
