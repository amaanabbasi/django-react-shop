# Generated by Django 2.2.4 on 2020-06-22 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20200622_1720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='itemPrice',
            new_name='itemPriceP',
        ),
    ]
