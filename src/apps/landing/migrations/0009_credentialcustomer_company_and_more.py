# Generated by Django 5.0 on 2024-06-06 01:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_alter_company_access_type'),
        ('landing', '0008_credentialsettings_remove_templatephoto_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentialcustomer',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_credentials', to='companies.company'),
        ),
        migrations.AlterField(
            model_name='credentialsettings',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_credential_settings', to='companies.company'),
        ),
    ]
