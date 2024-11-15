# Generated by Django 5.1 on 2024-08-20 09:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_barcode_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='level',
            field=models.CharField(choices=[('country', 'Country'), ('state', 'State'), ('city', 'City'), ('department', 'Department'), ('room', 'Room')], default='country', max_length=20),
        ),
        migrations.AddField(
            model_name='location',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='myapp.location'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('barcode', models.CharField(blank=True, max_length=255, unique=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='myapp.location')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_entries', to='myapp.asset')),
            ],
        ),
        migrations.DeleteModel(
            name='barcode',
        ),
    ]
