# Generated by Django 5.0 on 2024-09-08 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0039_usercompany_allow_networking_usercompany_in_person_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercompany',
            options={'verbose_name': 'Usuario de Compañía', 'verbose_name_plural': 'Usuarios de Compañías'},
        ),
    ]