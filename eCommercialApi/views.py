from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import  MultiPartParser
from .models import Category, Product, ProductAttribute, User
from .paginators import ProductPaginator
from .serializers import CategorySerializer, ProductSerializer, ProductAttributeSerializer, ProductDetailSerializer, UserSerializer


class UserViewSet(viewsets.ViewSet,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]

    #     return [permissions.IsAuthenticated()]

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


class ProductAttributeViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = ProductAttribute.objects.filter(active=True)
    serializer_class = ProductAttributeSerializer


def index(request):
    return render(request, template_name='index.html', context={
        "name": 'Long Phú'
    })
