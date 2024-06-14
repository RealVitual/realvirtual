# Generated by Django 5.0 on 2024-05-30 02:48

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_company_is_private_alter_company_is_virtual'),
        ('landing', '0003_remove_sponsor_description_remove_sponsor_video_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInvitedLanding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('names', models.CharField(blank=True, max_length=30, null=True, verbose_name='names')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='first name')),
                ('first_surname', models.CharField(blank=True, max_length=30, null=True, verbose_name='first surname')),
                ('last_surname', models.CharField(blank=True, max_length=30, null=True, verbose_name='last surname')),
                ('custom_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='custom url')),
                ('custom_image_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='custom image url')),
                ('is_present', models.BooleanField(default=False, verbose_name='Is Present')),
                ('is_virtual', models.BooleanField(default=False, verbose_name='Is Virtual')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invited_customers', to='companies.company')),
            ],
            options={
                'verbose_name': 'Invitado Landing',
                'verbose_name_plural': 'Invitados Landing',
                'ordering': ['-modified'],
            },
        ),
    ]
