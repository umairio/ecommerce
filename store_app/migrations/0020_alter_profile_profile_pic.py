# Generated by Django 5.0.3 on 2024-04-17 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0019_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='media/profile_pics', verbose_name='profile picture'),
        ),
    ]
