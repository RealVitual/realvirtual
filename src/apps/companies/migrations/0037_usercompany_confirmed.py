# Generated by Django 5.0 on 2024-09-03 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0036_usercompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercompany',
            name='confirmed',
            field=models.BooleanField(default=True, verbose_name='email confirmed?'),
        ),
    ]
