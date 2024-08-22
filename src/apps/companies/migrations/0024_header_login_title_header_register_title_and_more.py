# Generated by Django 5.0 on 2024-08-21 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0023_company_enable_credentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='header',
            name='login_title',
            field=models.CharField(default='Inicia Sesión', max_length=20, verbose_name='Título Login'),
        ),
        migrations.AddField(
            model_name='header',
            name='register_title',
            field=models.CharField(default='Regístrate', max_length=20, verbose_name='Título Registro'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='exhibitors_section_name',
            field=models.CharField(blank=True, default='Expositores', max_length=255, verbose_name='Expositores nombre Sección'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='networking_description_text',
            field=models.CharField(blank=True, default='Networking', max_length=255, verbose_name='Networking descripción texto'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='networking_section_name',
            field=models.CharField(blank=True, default='Networking', max_length=255, verbose_name='Networking nombre Sección'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='schedule_section_name',
            field=models.CharField(blank=True, default='Agenda', max_length=255, verbose_name='Agenda nombre Sección'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='schedule_section_title',
            field=models.CharField(blank=True, default='Programas y Ponentes', max_length=255, verbose_name='Agenda título Sección'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='sponsors_section_name',
            field=models.CharField(blank=True, default='Empresa', max_length=255, verbose_name='Auspiciadores nombre Sección'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='survey_description_text',
            field=models.CharField(blank=True, default='Por favor, ayúdanos a mejorar nuestra atención completando la siguiente encuesta.', max_length=255, verbose_name='Encuesta descripción texto'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='survey_section_name',
            field=models.CharField(blank=True, default='Tu opinión es importante', max_length=255, verbose_name='Encuesta nombre Sección'),
        ),
    ]