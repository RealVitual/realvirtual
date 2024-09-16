from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (
     AdminCustomerViewSet, )

app_name = 'companies'

router = DefaultRouter()
router.register(
    'customers_list',
    AdminCustomerViewSet)
urlpatterns = [
]

urlpatterns += router.urls
