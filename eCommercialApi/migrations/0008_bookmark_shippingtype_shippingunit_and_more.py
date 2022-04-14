# Generated by Django 4.0.3 on 2022-04-12 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0007_alter_product_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Standard', max_length=20)),
                ('minDate', models.IntegerField(default=1)),
                ('maxDate', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(null=True, upload_to='uploads/%Y/%m')),
                ('telephone', models.CharField(default='000000000', max_length=12)),
            ],
        ),
        migrations.AddField(
            model_name='productattribute',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='ShippingContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=255)),
                ('addressType', models.CharField(default='Home', max_length=255)),
                ('defaultAddress', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0.0)),
                ('detail', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eCommercialApi.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('unitPrice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eCommercialApi.productattribute')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shippedDate', models.DateTimeField(auto_now_add=True)),
                ('deliveryPrice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('shippedPrice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('discount', models.FloatField(default=0)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('status', models.IntegerField(default=1, max_length=1)),
                ('shippingType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eCommercialApi.shippingtype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookmarkDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmark', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eCommercialApi.bookmark')),
                ('productAttribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eCommercialApi.productattribute')),
            ],
        ),
    ]