# Generated by Django 5.0 on 2024-06-22 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0013_alter_company_logo_alter_homepage_home_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='date_description',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Date description'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='time_description',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Time description'),
        ),
    ]
