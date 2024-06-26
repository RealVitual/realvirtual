# Generated by Django 5.0 on 2024-06-26 03:22

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0016_company_mobile_banner'),
        ('landing', '0018_alter_credentialcustomer_credential_img_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('position', models.PositiveIntegerField(default=1, verbose_name='Posición')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name')),
                ('date_time', models.CharField(blank=True, max_length=255, verbose_name='Date and time')),
                ('addreess', models.CharField(blank=True, max_length=255, verbose_name='Address')),
                ('image', models.ImageField(blank=True, null=True, upload_to='test_realvirtual/videos/', verbose_name='Imagen')),
                ('link', models.CharField(blank=True, max_length=255, verbose_name='Link')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='external_events', to='companies.company')),
            ],
            options={
                'verbose_name': 'External event',
                'verbose_name_plural': 'External events',
            },
        ),
    ]
