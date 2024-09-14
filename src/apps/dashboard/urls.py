from django.urls import path, include, re_path
from .views import DashboardView, LoginView, LogoutView


app_name = "dashboard"

urlpatterns = [
     path('', DashboardView.as_view(), name='dashboard'),
     path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
   ]
