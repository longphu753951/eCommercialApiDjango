# Generated by Django 4.0.3 on 2022-04-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0005_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telephone',
            field=models.CharField(default='000000000', max_length=12),
        ),
    ]
