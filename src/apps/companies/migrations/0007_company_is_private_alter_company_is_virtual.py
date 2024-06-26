# Generated by Django 5.0 on 2024-05-29 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_remove_itemmainevent_main_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Is Private'),
        ),
        migrations.AlterField(
            model_name='company',
            name='is_virtual',
            field=models.BooleanField(default=True, verbose_name='Is virtual'),
        ),
    ]
