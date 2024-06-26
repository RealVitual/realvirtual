# Generated by Django 5.0 on 2024-06-05 04:52

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_rename_is_present_customerinvitedlanding_in_person_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplatePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('html_code', models.TextField(blank=True, verbose_name='Código HTML')),
                ('zoom', models.PositiveIntegerField(default=1, verbose_name='Zoom')),
                ('crop_h', models.PositiveIntegerField(default=0, verbose_name='Crop-h')),
                ('crop_w', models.PositiveIntegerField(default=0, verbose_name='Crop-w')),
                ('crop_x', models.PositiveIntegerField(default=0, verbose_name='Crop-x')),
                ('crop_y', models.PositiveIntegerField(default=0, verbose_name='Crop-y')),
            ],
            options={
                'verbose_name': 'Plantilla Imagen',
                'verbose_name_plural': 'Plantillas Imagen',
            },
        ),
        migrations.CreateModel(
            name='TemplateToImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('html_code', models.TextField(blank=True, verbose_name='Código HTML')),
            ],
            options={
                'verbose_name': 'Plantilla HTML a Imagen',
                'verbose_name_plural': 'Plantilla HTML a Imagen',
            },
        ),
        migrations.CreateModel(
            name='CredentialCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('names', models.CharField(blank=True, max_length=100, null=True, verbose_name='names')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_img', verbose_name='Imagen Perfil')),
                ('credential_img', models.ImageField(blank=True, null=True, upload_to='credentials', verbose_name='credential')),
                ('code', models.CharField(max_length=255, null=True, verbose_name='Codigo de acceso URL')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credentials', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Credencial',
                'verbose_name_plural': 'Credenciales',
                'ordering': ['-modified'],
            },
        ),
    ]
