from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Schedule, Workshop
from .utils import generate_ics_file, generate_workshop_ics_file


@receiver(pre_save, sender=Schedule)
def do_something_if_changed(sender, instance, update_fields, **kwargs):
    if not update_fields:
        try:
            obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            if not (obj.name == instance.name) or \
                not (obj.start_time == instance.start_time) or \
                    not (obj.end_time == instance.end_time):
                generate_ics_file(instance)
            if not obj.ics_file:
                generate_ics_file(instance)


@receiver(pre_save, sender=Workshop)
def do_something_if_workshop_changed(sender, instance, update_fields, **kwargs):
    if not update_fields:
        try:
            obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            if instance.start_datetime and instance.end_datetime:
                if not (obj.name == instance.name) or \
                    not (obj.start_datetime == instance.start_datetime) or \
                        not (obj.end_datetime == instance.end_datetime):
                    generate_workshop_ics_file(instance)
                if not obj.ics_file:
                    generate_workshop_ics_file(instance)
