# Generated by Django 5.0 on 2024-09-30 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_event_chat_code_event_chat_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='schedule_file',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='File'),
        ),
    ]
