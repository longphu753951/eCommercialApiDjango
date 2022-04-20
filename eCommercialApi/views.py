from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, status, permissions
from .models import Category, Product, ProductAttribute
from .paginators import ProductPaginator
from .serializers import CategorySerializer, ProductSerializer, ProductAttributeSerializer

class CategoryViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPaginator

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class ProductAttributeViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = ProductAttribute.objects.filter(active = True)
    serializer_class = ProductAttributeSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

def index(request):
    return render(request,template_name='index.html', context= {
        "name": 'Long Phú'
    })