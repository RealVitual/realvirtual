# Generated by Django 5.0 on 2024-09-05 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0037_usercompany_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
    ]