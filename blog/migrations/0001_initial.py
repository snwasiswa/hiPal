# Generated by Django 3.2.4 on 2021-07-23 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique_for_date='published_date')),
                ('blog_body', models.TextField()),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')],
                                            default='draft',
                                            max_length=15)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='blog_posts',
                                             to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.',
                                                         through='taggit.TaggedItem',
                                                         to='taggit.Tag',
                                                         verbose_name='Tags')),
            ],
            options={
                'ordering': ('-published_date',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('blog_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='comments',
                                                to='blog.blogpost')),
            ],
            options={
                'ordering': ('created_date',),
            },
        ),
    ]
