# Generated by Django 4.0.1 on 2022-01-16 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0018_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='files'),
        ),
    ]
