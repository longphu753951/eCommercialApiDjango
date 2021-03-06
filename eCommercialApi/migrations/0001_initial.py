# Generated by Django 4.0.3 on 2022-04-27 08:42

import colorfield.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(upload_to='img/users/%Y/%m')),
                ('telephone', models.CharField(max_length=12, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image_outline', models.ImageField(default=None, upload_to='img/categories/%Y/%m')),
                ('image_solid', models.ImageField(default=None, upload_to='img/categories/%Y/%m')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('rating', models.FloatField(default=0.0)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='eCommercialApi.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('sku', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=100)),
                ('hexColor', colorfield.fields.ColorField(default='#ffffff', image_field=None, max_length=18, samples=None)),
                ('sale_off', models.FloatField(null=True)),
                ('on_stock', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('active', models.BooleanField(default=False)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productAttribute', to='eCommercialApi.product')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(null=True, upload_to='img/shipping units/%Y/%m')),
                ('telephone', models.CharField(default='000000000', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Standard', max_length=20)),
                ('min_date', models.IntegerField(default=1)),
                ('max_date', models.IntegerField(default=1)),
                ('price_per_Km', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('shipping_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eCommercialApi.shippingunit')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=255)),
                ('address_type', models.CharField(default='Home', max_length=255)),
                ('default_address', models.BooleanField(default=False)),
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
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='img/products/%Y/%m')),
                ('productAttribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productImage', to='eCommercialApi.productattribute')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product_attribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eCommercialApi.productattribute')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipped_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('shipped_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('discount', models.FloatField(default=0)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('status', models.IntegerField(default=1, max_length=1)),
                ('shipping_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eCommercialApi.shippingtype')),
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
