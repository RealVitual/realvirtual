# Generated by Django 5.0 on 2024-08-14 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_event_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitor',
            name='organization',
            field=models.CharField(blank=True, max_length=255, verbose_name='Organización'),
        ),
    ]