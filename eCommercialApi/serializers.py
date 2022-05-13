from django.db.models import Min
from rest_framework import serializers
from .models import Category, Product, ProductAttribute, ProductImage, User, Bookmark, BookmarkDetail


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
    bookmarkDetail = BookmarkDetailSerializer(many=True, read_only=True)

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
        fields = ['id', 'first_name', 'password', 'last_name', 'username', 'email', 'telephone', 'avatar',
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
        print(validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()

        return user
