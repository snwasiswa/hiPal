# Generated by Django 3.2.4 on 2021-09-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0007_auto_20210908_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
