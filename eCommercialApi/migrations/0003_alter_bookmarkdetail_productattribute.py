# Generated by Django 4.0.3 on 2022-05-12 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eCommercialApi', '0002_alter_bookmark_user_alter_bookmarkdetail_bookmark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarkdetail',
            name='productAttribute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productAttribute', to='eCommercialApi.productattribute'),
        ),
    ]
