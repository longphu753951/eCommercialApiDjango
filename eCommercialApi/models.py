from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/%Y/%m")


class Category(models.Model):
    firsName = models.CharField(max_length=100, null=False, unique=True)
    lastName = models.CharField(max_length=100, null=False, unique=True)
    email = models.EmailField(max_length=100, null= False, unique=True)
    avatar = models.ImageField(upload_to="categories/%Y/%m", null=True)


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    rating = models.FloatField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)