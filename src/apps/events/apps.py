from django.apps import AppConfig


class EventConfig(AppConfig):
    name = 'src.apps.events'
    verbose_name = 'Eventos y Talleres'

    def ready(self):
        import src.apps.events.signals
