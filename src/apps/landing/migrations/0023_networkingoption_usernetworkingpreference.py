# Generated by Django 5.0 on 2024-08-11 21:18

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0019_header_show_more_events'),
        ('landing', '0022_surverychoicequestion_image_usersurveyanswer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_networking_options', to='companies.company')),
            ],
            options={
                'verbose_name': 'Opción de Networking',
                'verbose_name_plural': 'Opciones de Networking',
            },
        ),
        migrations.CreateModel(
            name='UserNetworkingPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_user_networking_preferences', to='companies.company')),
                ('networking_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='networking_user_preferences', to='landing.networkingoption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='networkin_preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Preferencia en Networking',
                'verbose_name_plural': 'Preferencias en Networking',
                'ordering': ['-modified'],
            },
        ),
    ]
