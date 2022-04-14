from django.contrib import admin
from .models import User, Category, Product, ProductAttribute, ProductImage, ShippingType, ShippingUnit
from django.utils.html import mark_safe
from django.contrib.auth.models import Permission

class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "rating","description", "category"]
    search_fields = [ "name", "category__name"]
    list_filter = ["category__name"]
    exclude = ['rating']

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["sku", "product", "color", "sale_off","on_stock", "active"]
    search_fields = [ "product__name"]
    list_filter = ["product__name"]


class ShippingUnitAdmin(admin.ModelAdmin):
    list_display = ["name", "image_tag", "telephone"]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product_attr", "image_tag"]
    search_fields = [ "product_attr__product__name", "product_attr__color"]
    list_filter = ["product_attr"]


class ShippingTypeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "min_date", "max_date", "price_per_Km"]
    search_fields = ["shipping_unit__name","type"]
    

#Register your models here.
admin.site.register(Permission)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ShippingUnit, ShippingUnitAdmin)
admin.site.register(ShippingType, ShippingTypeAdmin)
admin.site.register(User)