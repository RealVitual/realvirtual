# Generated by Django 5.0 on 2024-06-04 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_customerinvitedlanding'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerinvitedlanding',
            old_name='is_present',
            new_name='in_person',
        ),
        migrations.RenameField(
            model_name='customerinvitedlanding',
            old_name='is_virtual',
            new_name='virtual',
        ),
    ]
