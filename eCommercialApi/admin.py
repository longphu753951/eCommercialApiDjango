from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductImage, ShippingType, ShippingUnit

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductImage)
admin.site.register(ShippingUnit)
admin.site.register(ShippingType)