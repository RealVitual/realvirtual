# Generated by Django 5.0 on 2024-09-11 04:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0043_company_message_confirm_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='message_confirm_user',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Mensaje confirmación'),
        ),
    ]