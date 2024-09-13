# Generated by Django 5.0 on 2024-09-13 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0046_company_css_fonts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre compañia')),
            ],
            options={
                'verbose_name': 'Font',
                'verbose_name_plural': 'Fonts',
            },
        ),
        migrations.RemoveField(
            model_name='company',
            name='css_fonts',
        ),
        migrations.AddField(
            model_name='company',
            name='font',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='css_font_companies', to='companies.font'),
        ),
    ]
