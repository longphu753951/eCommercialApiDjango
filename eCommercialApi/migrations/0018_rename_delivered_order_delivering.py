# Generated by Django 4.0.3 on 2022-07-06 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0017_order_delivered'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='delivered',
            new_name='delivering',
        ),
    ]
