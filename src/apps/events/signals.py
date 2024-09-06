from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Schedule
from .utils import generate_ics_file


@receiver(pre_save, sender=Schedule)
def do_something_if_changed(sender, instance, update_fields, **kwargs):
    print('do_something_if_changed')
    if not update_fields:
        try:
            obj = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            print('SENDER DOES NOT EXIST')
            pass
        else:
            if not (obj.name == instance.name) or \
                not (obj.start_time == instance.start_time) or \
                    not (obj.end_time == instance.end_time):
                generate_ics_file(instance)
            if not obj.ics_file:
                generate_ics_file(instance)
