# Generated by Django 4.0.3 on 2022-04-26 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0023_product_defaultprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='defaultImage',
        ),
        migrations.RemoveField(
            model_name='product',
            name='defaultPrice',
        ),
    ]
