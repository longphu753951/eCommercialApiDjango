# Generated by Django 4.0.3 on 2022-06-22 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0011_remove_shippingcontact_default_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingcontact',
            name='telephone',
            field=models.CharField(default='', max_length=12),
        ),
    ]