from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import User, Category, Product, ProductAttribute, ProductImage, ShippingType, ShippingUnit, Bookmark
from django.contrib.auth.models import Permission


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "rating", "description", "category"]
    search_fields = ["name", "category__name"]
    list_filter = ["category__name"]
    exclude = ['rating']


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["sku", "product", "color", "sale_off", "on_stock", "active"]
    search_fields = ["product__name"]
    list_filter = ["product__name"]


class ShippingUnitAdmin(admin.ModelAdmin):
    list_display = ["name", "image_tag", "telephone"]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["productAttribute", "image"]
    search_fields = ["productAttribute__product__name", "productAttribute__color"]
    list_filter = ["productAttribute"]


class ShippingTypeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "min_date", "max_date", "price_per_Km"]
    search_fields = ["shipping_unit__name", "type"]


class BookmarkTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


class eCommercialAdminSite(admin.AdminSite):
    site_header = 'eCommercialApp'
    site_title = 'eCommercialApp'


admin_site = eCommercialAdminSite('eCommercialApi')

# Register your models here.
admin_site.register(Permission)
admin_site.register(Category)
admin_site.register(Product, ProductAdmin)
admin_site.register(ProductAttribute, ProductAttributeAdmin)
admin_site.register(ProductImage, ProductImageAdmin)
admin_site.register(ShippingUnit, ShippingUnitAdmin)
admin_site.register(ShippingType, ShippingTypeAdmin)
admin_site.register(Bookmark, BookmarkTypeAdmin)
admin_site.register(User)
admin_site.register(Group)
