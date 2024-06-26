# Generated by Django 5.0 on 2024-04-21 20:40

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_remove_homepage_main_event_subtitle_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemmainevent',
            name='main_description',
        ),
        migrations.AddField(
            model_name='itemmainevent',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='itemmainevent',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'),
        ),
    ]
