# Generated by Django 2.2.4 on 2020-06-18 10:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200618_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='upc',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
    ]
