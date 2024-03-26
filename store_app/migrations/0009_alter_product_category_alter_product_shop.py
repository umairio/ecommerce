# Generated by Django 5.0 on 2024-03-14 22:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0008_alter_product_category_alter_product_seller_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store_app.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store_app.shop'),
        ),
    ]
