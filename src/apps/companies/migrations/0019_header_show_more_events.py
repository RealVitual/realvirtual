# Generated by Django 5.0 on 2024-08-09 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0018_footer_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='header',
            name='show_more_events',
            field=models.BooleanField(default=True, verbose_name='Mostrar Más eventos'),
        ),
    ]
