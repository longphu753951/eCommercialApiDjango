# Generated by Django 4.0.3 on 2022-06-23 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0012_shippingcontact_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='default_address',
            field=models.CharField(default='', max_length=255),
        ),
    ]
