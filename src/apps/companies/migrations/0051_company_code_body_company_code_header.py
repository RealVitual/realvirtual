# Generated by Django 5.0 on 2024-09-20 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0050_company_company_position_names_field_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='code_body',
            field=models.TextField(blank=True, null=True, verbose_name='Código seguimiento BODY'),
        ),
        migrations.AddField(
            model_name='company',
            name='code_header',
            field=models.TextField(blank=True, null=True, verbose_name='Código seguimiento HEAD'),
        ),
    ]
