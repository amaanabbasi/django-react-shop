# Generated by Django 2.2.4 on 2020-06-20 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20200620_1528'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refund',
            old_name='accepted',
            new_name='granted',
        ),
    ]
