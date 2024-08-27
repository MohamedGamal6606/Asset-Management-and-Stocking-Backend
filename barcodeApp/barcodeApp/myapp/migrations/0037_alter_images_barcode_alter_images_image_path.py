# Generated by Django 5.1 on 2024-08-27 12:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='barcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.barcode'),
        ),
        migrations.AlterField(
            model_name='images',
            name='image_path',
            field=models.ImageField(upload_to='barcodes/'),
        ),
    ]
