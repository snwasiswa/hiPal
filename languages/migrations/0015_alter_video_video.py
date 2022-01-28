# Generated by Django 4.0.1 on 2022-01-16 02:39

import cloudinary_storage.storage
import cloudinary_storage.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0014_alter_file_file_alter_image_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(blank=True, default=None, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='videos', validators=[cloudinary_storage.validators.validate_video]),
        ),
    ]