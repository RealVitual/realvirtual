# Generated by Django 5.0 on 2024-06-22 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0015_company_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='mobile_banner',
            field=models.ImageField(blank=True, null=True, upload_to='test_realvirtual/mobile_banner/', verbose_name='Mobile Banner'),
        ),
    ]
