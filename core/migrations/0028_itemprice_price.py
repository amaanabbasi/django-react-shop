# Generated by Django 2.2.4 on 2020-06-23 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_itemprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemprice',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]