# Generated by Django 4.2.3 on 2023-08-15 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApi', '0003_cartlist_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='country',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='mobile',
            field=models.TextField(max_length=15),
        ),
    ]