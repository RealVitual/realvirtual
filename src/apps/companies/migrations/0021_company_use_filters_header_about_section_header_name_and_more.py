# Generated by Django 5.0 on 2024-08-20 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0020_header_show_exhibitors_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='use_filters',
            field=models.BooleanField(default=False, verbose_name='Usa filtros'),
        ),
        migrations.AddField(
            model_name='header',
            name='about_section_header_name',
            field=models.CharField(default='Acerca de', max_length=20, verbose_name='Nombre Acerca De Header'),
        ),
        migrations.AddField(
            model_name='header',
            name='exhibitors_header_name',
            field=models.CharField(default='Expositores', max_length=20, verbose_name='Nombre Expositores Header'),
        ),
        migrations.AddField(
            model_name='header',
            name='gallery_header_name',
            field=models.CharField(default='Galería', max_length=20, verbose_name='Nombre Galería Header'),
        ),
        migrations.AddField(
            model_name='header',
            name='networking_header_name',
            field=models.CharField(default='Networking', max_length=20, verbose_name='Nombre Networking Header'),
        ),
        migrations.AddField(
            model_name='header',
            name='schecule_header_name',
            field=models.CharField(default='Agenda', max_length=20, verbose_name='Nombre Horario Header'),
        ),
        migrations.AddField(
            model_name='header',
            name='sponsors_header_name',
            field=models.CharField(default='Auspiciadores', max_length=20, verbose_name='Nombre Auspiciadores Header'),
        ),
        migrations.AddField(
            model_name='header',
            name='survey_header_name',
            field=models.CharField(default='Encuesta', max_length=20, verbose_name='Nombre Encuesta Header'),
        ),
    ]
