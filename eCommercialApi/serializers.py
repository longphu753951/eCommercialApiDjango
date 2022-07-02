import stripe
from django.db.models import Min
from rest_framework import serializers
from .models import Category, Product, ProductAttribute, ProductImage, User, Bookmark, BookmarkDetail, ShippingContact, \
    OrderDetail, Order, Payment, ShippingUnit, ShippingType


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
    name = serializers.CharField(source='__str__')
    productImage = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ["sku", "color", "hexColor", "sale_off", "on_stock", "price", "active", "name", "productImage"]


class ProductSerializer(serializers.ModelSerializer):
    productAttribute = serializers.SerializerMethodField('get_productAttribute')

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


class BookmarkDetailSerializer(serializers.ModelSerializer):
    productAttribute = ProductAttributeSerializer()

    class Meta:
        model = BookmarkDetail
        fields = ["id", "bookmark", "productAttribute"]


class BookmarkDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkDetail
        fields = ["id", "bookmark", "productAttribute"]


class BookmarkSerializer(serializers.ModelSerializer):
    bookmarkDetail = serializers.SerializerMethodField(source='get_bookmarkDetail')
    bookmark = Bookmark.objects

    def get_bookmarkDetail(self, bookmark):
        bookmarkDetail = BookmarkDetail.objects
        serializer_context = {'request': self.context.get('request')}
        source = bookmarkDetail.filter(bookmark=bookmark)
        return BookmarkDetailSerializer(instance=source, many=True, context=serializer_context).data

    class Meta:
        model = Bookmark
        fields = ["id", "bookmarkDetail"]


class UserSerializer(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField(source='avatar')
    bookmark = serializers.SerializerMethodField('get_bookmark')
    user = User.objects

    def get_bookmark(self, user):
        bookmark = Bookmark.objects
        serializer_context = {'request': self.context.get('request')}
        source = bookmark.get(user=user)
        return BookmarkSerializer(instance=source, many=False, context=serializer_context).data

    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith('/static'):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'password', 'last_name', 'username', 'email', 'telephone', 'avatar',
                  "default_address",
                  'avatar_path', 'bookmark']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'avatar_path': {
                'read_only': True
            }, 'avatar': {
                'write_only': True
            }
        }


class ShippingContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingContact
        fields = ['id', 'name', 'district', 'ward', 'province', 'address', 'telephone']


class CreateUserSerializer(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField(source='avatar')
    user = User.objects

    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith('/static'):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'password', 'last_name', 'username', 'email', 'telephone', 'stripe_id', 'avatar',
                  'avatar_path']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'avatar_path': {
                'read_only': True
            }, 'avatar': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(**validated_data)
        print(user)
        user.set_password(validated_data['password'])
        user.save()

        return user


class OrderDetailSerializer(serializers.ModelSerializer):
    product_attribute = serializers.SerializerMethodField('get_productAttribute')
    final_price = serializers.SerializerMethodField('get_total_item_price')

    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'ordered',
            'product_attribute',
            'quantity',
            'final_price'
        )

    def get_productAttribute(self, obj):
        serializer_context = {'request': self.context.get('request')}
        return ProductAttributeSerializer(obj.product_attribute, context=serializer_context).data

    def get_total_item_price(self, obj):
        return obj.get_total_item_price()


class OrderSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_details',
            'total',
        )

    def get_order_details(self, obj):
        serializer_context = {'request': self.context.get('request')}
        return OrderDetailSerializer(obj.order_details.all(), many=True, context=serializer_context).data

    def get_total(self, obj):
        return obj.get_total()


class ShippingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingType
        fields = (
            'id',
            'type',
            'min_date',
            'max_date',
            'price_per_Km'
        )


class ShippingUnitSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    shipping_types = serializers.SerializerMethodField()

    def get_shipping_types(self, obj):
        serializer_context = {'request': self.context.get('request')}
        return ShippingTypeSerializer(ShippingType.objects.filter(shipping_unit=obj), many=True,
                                      context=serializer_context).data

    def get_image(self, obj):
        request = self.context['request']
        if obj.image and not obj.image.name.startswith('/static'):
            path = '/static/%s' % obj.image.name

            return request.build_absolute_uri(path)

    class Meta:
        model = ShippingUnit
        fields = (
            'id',
            'name',
            'image',
            'shipping_types',
            'telephone'
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'amount',
            'timestamp'
        )
