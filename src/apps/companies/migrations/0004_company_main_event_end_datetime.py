# Generated by Django 5.0 on 2024-04-21 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_company_in_person_company_is_virtual_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='main_event_end_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Main event datetime'),
        ),
    ]
