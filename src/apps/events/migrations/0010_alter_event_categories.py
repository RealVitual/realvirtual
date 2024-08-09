# Generated by Django 5.0 on 2024-08-09 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_filter_category_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='category_eventos', to='events.category'),
        ),
    ]
