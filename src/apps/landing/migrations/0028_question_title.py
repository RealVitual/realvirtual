# Generated by Django 5.0 on 2024-09-19 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0027_credentialsettings_first_text_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(default='Elige un regalo', max_length=255, verbose_name='Titulo'),
        ),
    ]
