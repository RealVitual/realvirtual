# Generated by Django 5.0 on 2024-08-28 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0025_alter_freeimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentialsettings',
            name='title_credential',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Titulo credencial'),
        ),
    ]
