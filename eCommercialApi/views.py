from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]


def index(request):
    return render(request,template_name='index.html', context= {
        "name": 'Long Phú'
    })