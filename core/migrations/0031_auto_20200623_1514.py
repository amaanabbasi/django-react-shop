# Generated by Django 2.2.4 on 2020-06-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_remove_itemordered_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_variations',
            field=models.ManyToManyField(blank=True, null=True, to='core.ItemVariation'),
        ),
    ]