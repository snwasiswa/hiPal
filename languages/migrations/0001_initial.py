# Generated by Django 3.2.4 on 2021-07-23 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import languages.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('outline', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='lessons_created',
                                              to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               related_name='lessons',
                                               to='languages.language')),
                ('student', models.ManyToManyField(blank=True,
                                                   related_name='lessons_joined',
                                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='videos')),
                ('url', models.URLField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='video_related',
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('order', languages.fields.OrderOfField(blank=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='units',
                                             to='languages.lesson')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='text_related',
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('picture', models.FileField(upload_to='images')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='image_related',
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='files')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='file_related',
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('order', languages.fields.OrderOfField(blank=True)),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('video', 'text', 'image', 'file')},
                                                   on_delete=django.db.models.deletion.CASCADE,
                                                   to='contenttypes.contenttype')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='contents',
                                           to='languages.unit')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]