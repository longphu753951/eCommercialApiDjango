from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from uuid import uuid4
from colorfield.fields import ColorField

from eCommercialApi import settings


class User(AbstractUser):
    avatar = models.ImageField(upload_to="img/users/%Y/%m")
    telephone = models.CharField(max_length=12, null=False, unique=True)
    default_address = models.CharField(null=False, default="", max_length=255)
    stripe_id = models.CharField(max_length=100, null=True, unique=True)


class ShippingContact(models.Model):
    name = models.CharField(max_length=255, null=False, default='')
    telephone = models.CharField(max_length=12, null=False, unique=False, default='')
    district = models.CharField(max_length=255, null=False, default='')
    ward = models.CharField(max_length=255, null=False, default='')
    province = models.CharField(max_length=255, null=False, default='')
    address = models.CharField(max_length=255, null=False, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image_outline = models.ImageField(null=False, default=None, upload_to='img/categories/%Y/%m')
    image_solid = models.ImageField(null=False, default=None, upload_to='img/categories/%Y/%m')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    rating = models.FloatField(null=False, default=0.0)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    sku = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    color = models.CharField(max_length=100, null=False)
    hexColor = ColorField(default='#ffffff')
    sale_off = models.FloatField(null=True)
    on_stock = models.IntegerField(null=False, default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    active = models.BooleanField(null=False, default=False)
    product = models.ForeignKey(Product, null=True, related_name='productAttribute', on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.name + " (" + self.color + ")"


class ProductImage(models.Model):
    image = models.ImageField(null=True, upload_to='img/products/%Y/%m')
    productAttribute = models.ForeignKey(ProductAttribute, null=True, related_name='productImage',
                                         on_delete=models.SET_NULL)

    def image_tag(self):
        return mark_safe('<img src="/static/%s" width="110" height="110"  />' % (self.image))


class Bookmark(models.Model):
    user = models.ForeignKey(User, null=True, related_name='bookmark', on_delete=models.SET_NULL)


class BookmarkDetail(models.Model):
    bookmark = models.ForeignKey(Bookmark, related_name='bookmarkDetail', on_delete=models.SET_NULL, null=True)
    productAttribute = models.ForeignKey(ProductAttribute, related_name='bookmarkDetail', on_delete=models.SET_NULL,
                                         null=True)


class ShippingUnit(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(null=True, upload_to='img/shipping units/%Y/%m')
    telephone = models.CharField(max_length=12, null=False, default='000000000')

    def image_tag(self):
        return mark_safe('<img src="/static/%s" width="150"  />' % (self.image))

    def __str__(self):
        return self.name


class ShippingType(models.Model):
    type = models.CharField(max_length=20, null=False, default="Standard")
    min_date = models.IntegerField(null=False, default=1)
    max_date = models.IntegerField(null=False, default=1)
    price_per_Km = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    shipping_unit = models.ForeignKey(ShippingUnit, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.shipping_unit.name + " (" + self.type + ")"


class Review(models.Model):
    rating = models.FloatField(null=False, default=0.0)
    detail = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, null=True, related_name='payment', on_delete=models.SET_NULL)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class OrderDetail(models.Model):
    user = models.ForeignKey(User, null=True, related_name='orderDetail', on_delete=models.SET_NULL)
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(null=False, default=1)

    def __str__(self):
        return f"{self.product_attribute.__str__()}"

    def get_total_item_price(self):
        return self.quantity * self.product_attribute.price


class Order(models.Model):
    user = models.ForeignKey(User, null=True, related_name='order', on_delete=models.SET_NULL)
    order_details = models.ManyToManyField(OrderDetail)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    shipping_contact = models.ForeignKey(ShippingContact, null=True, related_name='shippingContact',
                                         on_delete=models.SET_NULL)
    shipping_type = models.ForeignKey(ShippingType, null=True, related_name='shippingType',
                                      on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_detail in self.order_details.all():
            total += order_detail.get_total_item_price()
        return total
