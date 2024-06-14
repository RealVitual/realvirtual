# Generated by Django 5.0 on 2024-06-07 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0015_ticketsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsettings',
            name='event_time',
            field=models.CharField(max_length=255, null=True, verbose_name='Hora evento'),
        ),
        migrations.AlterField(
            model_name='ticketsettings',
            name='event_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Nombre evento'),
        ),
    ]
