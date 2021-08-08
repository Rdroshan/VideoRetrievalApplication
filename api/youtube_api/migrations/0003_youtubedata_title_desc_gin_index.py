# Generated by Django 3.2.6 on 2021-08-08 19:42

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_api', '0002_install_trigram_ext'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='youtubedata',
            index=django.contrib.postgres.indexes.GinIndex(fields=['title', 'description'], name='title_desc_gin_index', opclasses=['gin_trgm_ops', 'gin_trgm_ops']),
        ),
    ]