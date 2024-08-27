# Generated by Django 5.1 on 2024-08-22 08:45

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_asset_inventory_alter_inventory_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset', to='myapp.inventory'),
        ),
        migrations.CreateModel(
            name='AssetCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AssetCount', to='myapp.asset')),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AssetCount', to='myapp.office')),
            ],
        ),
    ]
