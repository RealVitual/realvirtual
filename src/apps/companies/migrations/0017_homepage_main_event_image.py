# Generated by Django 5.0 on 2024-08-09 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0016_company_mobile_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='main_event_image',
            field=models.ImageField(blank=True, null=True, upload_to='test_realvirtual/main_event_image/', verbose_name='Main Event image'),
        ),
    ]
