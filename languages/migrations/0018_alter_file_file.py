# Generated by Django 4.0.1 on 2022-01-16 04:26

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0017_alter_video_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='files'),
        ),
    ]