# Generated by Django 5.0 on 2024-10-29 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_alter_ticket_pdf_alter_ticket_qr'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-created'], 'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
    ]