# Generated by Django 5.0 on 2024-08-21 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0022_company_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='enable_credentials',
            field=models.BooleanField(default=False, verbose_name='Habilitar credenciales'),
        ),
    ]