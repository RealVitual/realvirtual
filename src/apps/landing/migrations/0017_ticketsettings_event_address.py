# Generated by Django 5.0 on 2024-06-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0016_ticketsettings_event_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsettings',
            name='event_address',
            field=models.CharField(max_length=255, null=True, verbose_name='Dirección evento'),
        ),
    ]
