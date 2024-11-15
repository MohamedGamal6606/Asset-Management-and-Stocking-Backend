# Generated by Django 5.1 on 2024-08-22 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_alter_area_governate_alter_building_area_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='location',
        ),
        migrations.AddField(
            model_name='asset',
            name='office',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset', to='myapp.office'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='inventory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assset', to='myapp.inventory'),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
