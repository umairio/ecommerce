# Generated by Django 5.0 on 2024-03-14 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_order_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Product',
            new_name='product',
        ),
    ]
