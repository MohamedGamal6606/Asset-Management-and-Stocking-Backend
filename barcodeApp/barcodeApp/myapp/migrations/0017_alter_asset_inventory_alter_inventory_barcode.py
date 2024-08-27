# Generated by Django 5.1 on 2024-08-22 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_remove_asset_location_asset_office_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assset', to='myapp.inventory'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='barcode',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
