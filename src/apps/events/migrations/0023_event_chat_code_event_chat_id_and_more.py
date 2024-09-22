# Generated by Django 5.0 on 2024-09-22 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_exhibitor_link_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='chat_code',
            field=models.CharField(blank=True, max_length=255, verbose_name='Codigo de chat'),
        ),
        migrations.AddField(
            model_name='event',
            name='chat_id',
            field=models.PositiveIntegerField(default=0, verbose_name='Id de chat'),
        ),
        migrations.AddField(
            model_name='event',
            name='open_transmission',
            field=models.BooleanField(default=False, verbose_name='Abrir transmision'),
        ),
    ]
