# Generated by Django 5.0 on 2024-09-26 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0054_enterprise_company_enterprise'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='background',
            field=models.CharField(default='#333', max_length=100, verbose_name='Background Color'),
        ),
    ]
