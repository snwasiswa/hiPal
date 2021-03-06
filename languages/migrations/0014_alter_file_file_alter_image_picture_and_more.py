# Generated by Django 4.0.1 on 2022-01-16 02:31

import ckeditor.fields
import cloudinary_storage.storage
import cloudinary_storage.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0013_alter_image_picture_alter_video_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='files'),
        ),
        migrations.AlterField(
            model_name='image',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='images'),
        ),
        migrations.AlterField(
            model_name='text',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.ImageField(blank=True, default=None, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='videos', validators=[cloudinary_storage.validators.validate_video]),
        ),
    ]
