from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'src.apps.users'

    def ready(self):
        import src.apps.users.signals # noqa: F401
