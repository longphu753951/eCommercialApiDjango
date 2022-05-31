"""eCommercialApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from .admin import admin_site
from django.shortcuts import redirect
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(prefix='categories', viewset=views.CategoryViewSet, basename='category')
router.register(prefix='products', viewset=views.ProductViewSet, basename='product')
router.register(prefix='productAttribute', viewset=views.ProductAttributeViewSet, basename='productAttribute')
router.register(prefix='bookmark', viewset=views.BookmarkViewSet, basename='bookmark')
router.register(prefix='bookmarkDetail', viewset=views.BookmarkDetailViewSet, basename='bookmarkDetail')
router.register('users', views.UserViewSet)


urlpatterns = [
    # path('',include('eCommercialApi.urls')),
    path('admin', admin_site.urls),
    # path('', lambda request: redirect('admin/', permanent=True))
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]
