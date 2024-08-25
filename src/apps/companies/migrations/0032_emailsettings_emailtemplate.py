# Generated by Django 5.0 on 2024-08-25 02:23

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import src.apps.companies.constants
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0031_company_cookies_policy_company_privacy_policy_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('host', models.CharField(blank=True, max_length=500, null=True, verbose_name='Email Host')),
                ('port', models.CharField(default=587, max_length=500, verbose_name='Email Port')),
                ('username', models.CharField(blank=True, max_length=500, null=True, verbose_name='Username Email')),
                ('password', models.CharField(blank=True, max_length=500, null=True, verbose_name='Password Email')),
                ('use_tls', models.BooleanField(default=True, verbose_name='Usa TLS')),
                ('schedule_mail', models.BooleanField(default=True, verbose_name='Enviar correo de agenda')),
                ('register_mail', models.BooleanField(default=True, verbose_name='Enviar correo de registro')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='email_settings', to='companies.company')),
            ],
            options={
                'verbose_name': 'Reglas de correo',
                'verbose_name_plural': 'Reglas de correo',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('email_type', models.CharField(choices=[('REGISTER', 'Registro completado'), ('PASSWORD', 'Recuperar/Reestablecer contraseña'), ('SCHEDULE', 'Confirmación de agenda')], default=src.apps.companies.constants.EmailType['REGISTER'], max_length=30, verbose_name='¿Para qué se usará el correo?')),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Nombre')),
                ('subject', models.CharField(max_length=128, verbose_name='Asunto')),
                ('html_code', models.TextField(blank=True, verbose_name='Código HTML')),
                ('from_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Emisor')),
                ('from_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre Emisor')),
                ('attach_file', models.BooleanField(default=False, verbose_name='Tiene adjunto')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='email_templates', to='companies.company')),
            ],
            options={
                'verbose_name': 'Plantilla Correo',
                'verbose_name_plural': 'Plantillas Correo',
            },
        ),
    ]
