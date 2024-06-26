# Generated by Django 5.0 on 2024-06-26 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0019_externalevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externalevent',
            name='date_time',
        ),
        migrations.AddField(
            model_name='externalevent',
            name='event_date',
            field=models.CharField(blank=True, max_length=255, verbose_name='Event date'),
        ),
        migrations.AddField(
            model_name='externalevent',
            name='event_time',
            field=models.CharField(blank=True, max_length=255, verbose_name='Event time'),
        ),
    ]
