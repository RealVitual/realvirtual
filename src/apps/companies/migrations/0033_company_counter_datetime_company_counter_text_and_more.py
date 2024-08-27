# Generated by Django 5.0 on 2024-08-27 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0032_emailsettings_emailtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='counter_datetime',
            field=models.DateTimeField(null=True, verbose_name='Fecha y Hora de contador'),
        ),
        migrations.AddField(
            model_name='company',
            name='counter_text',
            field=models.CharField(blank=True, default='Evento disponible en', max_length=255, null=True, verbose_name='Texto contador'),
        ),
        migrations.AddField(
            model_name='company',
            name='use_counter',
            field=models.BooleanField(default=False, verbose_name='Usa Contador'),
        ),
    ]
