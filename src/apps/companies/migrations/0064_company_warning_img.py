# Generated by Django 5.0 on 2024-10-18 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0063_homepage_gallery_section_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='warning_img',
            field=models.ImageField(blank=True, null=True, upload_to='test_realvirtual/warning_img/', verbose_name='Imagen aviso'),
        ),
    ]