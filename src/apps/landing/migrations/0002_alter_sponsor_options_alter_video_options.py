# Generated by Django 5.0 on 2024-05-15 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsor',
            options={'verbose_name': 'Sponsor', 'verbose_name_plural': 'Sponsors'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
    ]
