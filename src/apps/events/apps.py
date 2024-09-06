from django.apps import AppConfig


class EventConfig(AppConfig):
    name = 'src.apps.events'

    def ready(self):
        import src.apps.events.signals
