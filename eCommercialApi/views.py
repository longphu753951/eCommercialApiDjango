from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Category, Product, ProductAttribute, User, Bookmark, BookmarkDetail
from .paginators import ProductPaginator
from .serializers import CategorySerializer, ProductSerializer, ProductAttributeSerializer, ProductDetailSerializer, \
    UserSerializer, BookmarkSerializer, CreateUserSerializer, BookmarkDetailSerializer, BookmarkDetailCreateSerializer


class UserViewSet(viewsets.ViewSet,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = CreateUserSerializer
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.AllowAny]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        context = super().get_serializer_context()
        return Response(UserSerializer(request.user, context=context).data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(id=serializer.data["id"])
        b = Bookmark(user=user)
        b.save()

        return Response('test', status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='product')
    # product/
    def get_product_by_category(self, query, pk):
        context = super().get_serializer_context()
        if int(pk) == 0:
            products = Product.objects.all()
        else:
            category = Category.objects.get(pk=pk)
            products = category.products.all()

        return Response(data=ProductSerializer(products, many=True, context=context).data,
                        status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    pagination_class = ProductPaginator

    # def get_permissions(self):
    # if self.action == 'list':
    # return [permissions.AllowAny()]

    # return [permissions.IsAuthenticated()]

    @action(methods=['get'], detail=True, url_path='productAttributes')
    # product/
    def get_product_attribute(self, query, pk):
        context = super().get_serializer_context()
        product = Product.objects.get(pk=pk)
        product_attributes = product.productAttribute.all()

        return Response(data=ProductAttributeSerializer(product_attributes, many=True, context=context).data,
                        status=status.HTTP_200_OK)


class BookmarkViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    serializer_class = BookmarkSerializer

    @action(methods=['get'], detail=True)
    # product/
    def get_queryset(self):
        context = super().get_serializer_context()

        user = self.request.user

        bookmark = Bookmark.objects.get(user=user)

        return Response(data=self.serializer_class(bookmark, many=False, context=context).data,
                        status=status.HTTP_200_OK)


class BookmarkDetailViewSet(viewsets.ModelViewSet, generics.CreateAPIView):
    serializer_class = BookmarkDetailCreateSerializer


class ProductAttributeViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = ProductAttribute.objects.filter(active=True)
    serializer_class = ProductAttributeSerializer


def index(request):
    return render(request, template_name='index.html', context={
        "name": 'Long Phú'
    })
