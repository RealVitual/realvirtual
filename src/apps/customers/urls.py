from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
     GenerateInvitedEmail, )

app_name = 'customers'

router = DefaultRouter()
urlpatterns = [
     path(
          'generate_landing_invited/', GenerateInvitedEmail.as_view(),
          name='generate_landing_invited'),
]

urlpatterns += router.urls
