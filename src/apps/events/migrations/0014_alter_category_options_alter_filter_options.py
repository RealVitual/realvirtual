# Generated by Django 5.0 on 2024-08-20 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_category_position_filter_created_filter_is_active_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['position'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='filter',
            options={'ordering': ['position'], 'verbose_name': 'Filter', 'verbose_name_plural': 'Filters'},
        ),
    ]