from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product, ProductAttribute
from .paginators import ProductPaginator
from .serializers import CategorySerializer, ProductSerializer, ProductAttributeSerializer


class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]

    #     return [permissions.IsAuthenticated()]

    @action(methods=['get'], detail=True, url_path='products')
    # product/
    def get_product_by_category(self, query, pk):
        context = super().get_serializer_context()
        category = Category.objects.get(pk=pk)
        products = category.products.all()

        return Response(data=ProductSerializer(products, many=True, context=context).data,
                        status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPaginator

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

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
