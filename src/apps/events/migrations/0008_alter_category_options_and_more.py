# Generated by Django 5.0 on 2024-08-01 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_category_event_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='parent',
        ),
    ]
