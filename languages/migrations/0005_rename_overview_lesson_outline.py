# Generated by Django 3.2.4 on 2021-07-19 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('languages', '0004_alter_lesson_language'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='overview',
            new_name='outline',
        ),
    ]
