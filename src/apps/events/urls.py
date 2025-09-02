from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
    GenerateScheduleCustomerEvent, GenerateWorkshopCustomerEvent)

app_name = 'events'

router = DefaultRouter()
# router.register('get_invit', CustomerEventPermission)
urlpatterns = [
     path(
         'generate_schedule/', GenerateScheduleCustomerEvent.as_view(),
         name='generate_schedule'),
     path(
         'generate_schedule_workshop/', GenerateWorkshopCustomerEvent.as_view(),
         name='generate_schedule_workshop'),
]

urlpatterns += router.urls
