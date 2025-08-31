from .models import Schedule
from ics import Calendar, Event
from ics.attendee import Organizer
from src.apps.companies.models import EmailTemplate
import tempfile
from datetime import datetime
import pytz
from django.core import files
from src.apps.companies.constants import EmailType
c = Calendar()
e = Event()


def generate_ics_file(schedule):
    company = schedule.event.company
    mail = EmailTemplate.objects.filter(
        company=company, email_type="SCHEDULE"
    ).last()
    if mail:
        c = Calendar()
        e = Event()
        organizer = Organizer(email=mail.from_email)
        e.name = "%s" % (schedule.name)
        e.organizer = organizer
        e.description = mail.description
        start_date = schedule.event.start_datetime.date()
        start_datetime = datetime.combine(
                    start_date, schedule.start_time).astimezone(pytz.utc)
        end_datetime = datetime.combine(
                    start_date, schedule.end_time).astimezone(pytz.utc)
        e.begin = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        e.end = end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        c.events.add(e)
        c.events
        fp = tempfile.TemporaryFile()
        with fp as f:
            f.write(str(c).encode())
            f.seek(0)
            temp_file = files.File(f, name='{}-{}.ics'.format(
                schedule.event.name.replace(' ', '_'),
                schedule.name.replace(' ', '_')))
            schedule.ics_file = temp_file
            schedule.save(update_fields=['ics_file'])
        fp.close()


def generate_workshop_ics_file(schedule):
    company = schedule.event.company
    mail = EmailTemplate.objects.filter(
        company=company, email_type="SCHEDULE"
    ).last()
    if mail:
        c = Calendar()
        e = Event()
        organizer = Organizer(email=mail.from_email)
        e.name = "%s" % (schedule.name)
        e.organizer = organizer
        e.description = mail.description
        start_date = schedule.event.start_datetime.date()
        start_datetime = datetime.combine(
                    start_date, schedule.start_time).astimezone(pytz.utc)
        end_datetime = datetime.combine(
                    start_date, schedule.end_time).astimezone(pytz.utc)
        e.begin = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        e.end = end_datetime.strftime("%Y-%m-%d %H:%M:%S")
        c.events.add(e)
        c.events
        fp = tempfile.TemporaryFile()
        with fp as f:
            f.write(str(c).encode())
            f.seek(0)
            temp_file = files.File(f, name='{}-{}.ics'.format(
                schedule.event.name.replace(' ', '_'),
                schedule.name.replace(' ', '_')))
            schedule.ics_file = temp_file
            schedule.save(update_fields=['ics_file'])
        fp.close()
