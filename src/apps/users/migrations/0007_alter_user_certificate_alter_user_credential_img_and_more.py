# Generated by Django 5.0 on 2024-06-20 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_full_name_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='certificate',
            field=models.FileField(blank=True, null=True, upload_to='test_realvirtual/certificates/', verbose_name='certificado'),
        ),
        migrations.AlterField(
            model_name='user',
            name='credential_img',
            field=models.ImageField(blank=True, null=True, upload_to='test_realvirtual/credentials/', verbose_name='credential'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='test_realvirtual/profile_img/', verbose_name='Imagen Perfil'),
        ),
    ]
