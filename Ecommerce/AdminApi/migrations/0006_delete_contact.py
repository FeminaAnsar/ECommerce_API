# Generated by Django 4.2.3 on 2023-08-15 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApi', '0005_remove_product_quantity_product_stock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
    ]