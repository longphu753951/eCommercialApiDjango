# Generated by Django 4.0.3 on 2022-06-28 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0015_order_order_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]
