# Generated by Django 5.1 on 2024-08-25 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_assetcount_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetcount',
            name='user',
        ),
    ]
