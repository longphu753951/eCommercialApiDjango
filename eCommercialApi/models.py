from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/%Y/%m")
    telephone = models.CharField(max_length=12, null=False, default='000000000')


class ShippingContact(models.Model):
    name = models.CharField(max_length=255, null=False, default='')
    address = models.CharField(max_length=255, null=False, default='')
    addressType = models.CharField(max_length=255, null=False, default='Home')
    defaultAddress = models.BooleanField(null=False, default=False)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(null=True, upload_to='uploads/%Y/%m')


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    rating = models.FloatField(null=False, default=0.0)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class ProductAttribute(models.Model):
    def __init__(self):
        pass

    sku = models.CharField(max_length=100, primary_key=True, unique=True)
    color = models.CharField(max_length=100, null=False)
    saleOff = models.FloatField(null=True)
    onStock = models.IntegerField(null=False, default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    active = models.BooleanField(null=False, default=False)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

class ProductImage(models.Model):
    def __init__(self):
        pass

    image = models.ImageField(null=True, upload_to='uploads/%Y/%m')
    productAttr = models.ForeignKey(ProductAttribute, null=True, on_delete=models.SET_NULL)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)


class BookmarkDetail(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.SET_NULL, null=True)
    productAttribute = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL, null=True)


class ShippingUnit(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image = models.ImageField(null=True, upload_to='uploads/%Y/%m')
    telephone = models.CharField(max_length=12, null=False, default='000000000')


class ShippingType(models.Model):
    type = models.CharField(max_length=20, null=False, default="Standard")
    minDate = models.IntegerField(null=False, default=1)
    maxDate = models.IntegerField(null=False, default=1)
    shippingUnit = models.ForeignKey(ShippingUnit, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    shippingType = models.ForeignKey(ShippingType, on_delete=models.SET_NULL, null=True)
    shippedDate = models.DateTimeField(auto_now_add=True, blank=True)
    deliveryPrice = models.DecimalField(max_digits = 5, decimal_places = 2)
    shippedPrice = models.DecimalField(max_digits = 5, decimal_places = 2)
    discount = models.FloatField(null =False, default=0)
    totalPrice = models.DecimalField(max_digits = 5, decimal_places = 2)
    status = models.IntegerField(max_length=1, null=False, default=1)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)


class OrderDetail(models.Model):
    product = models.ForeignKey(ProductAttribute, on_delete= models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False, default=1)
    unitPrice = models.DecimalField(max_digits = 5, decimal_places = 2)


class Review(models.Model):
    rating = models.FloatField(null=False, default=0.0)
    detail = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)








    

