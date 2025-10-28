from django.contrib import admin
from .models import DummyLink


@admin.register(DummyLink)
class DummyLinkAdmin(admin.ModelAdmin):
    # Ocultamos la opción "Añadir"
    def has_add_permission(self, request):
        return False

    # Ocultamos la opción "Ver" lista
    def has_view_permission(self, request, obj=None):
        return False

    # Ocultamos la sección en el admin por si acaso
    def get_model_perms(self, request):
        return {}

    # El método más simple para ocultarlo de la interfaz del Admin:
    def get_urls(self):
        return []
