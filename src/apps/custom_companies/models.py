from django.db import models


class DummyLink(models.Model):
    # Este modelo es solo un marcador de posición.
    # No necesita campos.
    class Meta:
        managed = False
        verbose_name = 'Enlace temporal'
        verbose_name_plural = 'Enlace temporal'
