# Generated by Django 5.0 on 2024-06-07 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_jon_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Full name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'El email ya se encuentra registrado.'}, max_length=254, null=True, unique=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_surname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='First surname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_surname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Last surname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='names',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Names'),
        ),
    ]
