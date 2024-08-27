# Generated by Django 5.1 on 2024-08-22 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_area_id_alter_building_id_alter_country_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='governate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='myapp.governate'),
        ),
        migrations.AlterField(
            model_name='building',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='myapp.area'),
        ),
        migrations.AlterField(
            model_name='governate',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='governates', to='myapp.country'),
        ),
        migrations.AlterField(
            model_name='office',
            name='Building',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offices', to='myapp.building'),
        ),
    ]
