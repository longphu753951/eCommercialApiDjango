# Generated by Django 4.0.3 on 2022-04-13 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0013_rename_image_category_image_outline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image_outline',
            field=models.ImageField(default=None, upload_to='categories/%Y/%m'),
        ),
    ]