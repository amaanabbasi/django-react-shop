# Generated by Django 2.2.4 on 2020-06-20 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20200620_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refund',
            name='granted',
        ),
    ]
