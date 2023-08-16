# Generated by Django 4.2.3 on 2023-08-16 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApi', '0008_alter_ordereditem_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartlist',
            name='order_status',
        ),
        migrations.AddField(
            model_name='checkout',
            name='order_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=20),
        ),
    ]
