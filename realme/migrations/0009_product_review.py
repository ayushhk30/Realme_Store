# Generated by Django 5.0.6 on 2024-07-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realme', '0008_product_battery_product_bluetooth_product_mic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='review',
            field=models.TextField(default=50),
            preserve_default=False,
        ),
    ]
