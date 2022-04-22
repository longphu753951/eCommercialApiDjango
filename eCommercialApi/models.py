from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from uuid import uuid4

class User(AbstractUser):
    avatar = models.ImageField(upload_to="img/users/%Y/%m")
    telephone = models.CharField(max_length=12, null=False, default='000000000')


class ShippingContact(models.Model):
    name = models.CharField(max_length=255, null=False, default='')
    address = models.CharField(max_length=255, null=False, default='')
    address_type = models.CharField(max_length=255, null=False, default='Home')
    default_address = models.BooleanField(null=False, default=False)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    image_outline = models.ImageField(null=False, default= None, upload_to='img/categories/%Y/%m')
    image_solid = models.ImageField(null=False, default= None,upload_to='img/categories/%Y/%m')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    rating = models.FloatField(null=False, default=0.0)
    description = models.TextField(null=True, blank=True)
    defaultImage = models.ImageField(null=True, upload_to='img/defaultImageProduct/%Y/%m')
    category = models.ForeignKey(Category,related_name="products", on_delete=models.SET_NULL, null=True)

    def image_tag(self):
        return mark_safe('<img src="/static/%s" width="110" height="110"  />' % self.defaultImage)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    sku = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    color = models.CharField(max_length=100, null=False)
    sale_off = models.FloatField(null=True)
    on_stock = models.IntegerField(null=False, default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    active = models.BooleanField(null=False, default=False)
    product = models.ForeignKey(Product, null=True, related_name='productAttribute', on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.name +" "+ self.color

class ProductImage(models.Model):
    image = models.ImageField(null=True, upload_to='img/products/%Y/%m')
    productAttribute = models.ForeignKey(ProductAttribute, null=True, related_name='productImage', on_delete=models.SET_NULL)

    def image_tag(self):
        return mark_safe('<img src="/static/%s" width="110" height="110"  />' % (self.image))


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)


class BookmarkDetail(models.Model):
    bookmark = models.ForeignKey(Bookmark, on_delete=models.SET_NULL, null=True)
    productAttribute = models.ForeignKey(ProductAttribute, on_delete=models.SET_NULL, null=True)




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
    price_per_Km = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0.0)
    shipping_unit = models.ForeignKey(ShippingUnit, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.shipping_unit.name + " (" + self.type +")"


class Order(models.Model):
    shipping_type = models.ForeignKey(ShippingType, on_delete=models.SET_NULL, null=True)
    shipped_date = models.DateTimeField(auto_now_add=True, blank=True)
    delivery_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    shipped_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    discount = models.FloatField(null =False, default=0)
    total_price = models.DecimalField(max_digits = 5, decimal_places = 2)
    status = models.IntegerField(max_length=1, null=False, default=1)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)


class OrderDetail(models.Model):
    product_attribute = models.ForeignKey(ProductAttribute, on_delete= models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False, default=1)
    unit_price = models.DecimalField(max_digits = 5, decimal_places = 2)


class Review(models.Model):
    rating = models.FloatField(null=False, default=0.0)
    detail = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)








    

