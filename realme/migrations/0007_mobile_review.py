# Generated by Django 5.0.6 on 2024-07-04 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realme', '0006_rename_color_mobile_camera_alter_mobile_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobile',
            name='review',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
