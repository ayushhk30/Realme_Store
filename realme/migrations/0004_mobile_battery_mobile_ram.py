# Generated by Django 5.0.6 on 2024-07-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realme', '0003_order_orderitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobile',
            name='battery',
            field=models.CharField(default=5000, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mobile',
            name='ram',
            field=models.CharField(default=8, max_length=255),
            preserve_default=False,
        ),
    ]
