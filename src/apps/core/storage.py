from django.conf import settings
from django.utils._os import safe_join
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    file_overwrite = False

    @property
    def location(self):
        media = 'media'
        location = '{}'.format(media)
        return location

    @location.setter
    def location(self, value):
        pass
