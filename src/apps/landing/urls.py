from django.urls import path
from .views import (
    HomeView, EventsView, GenerateCredentialView, validate_register,
    confirm_register, SelectPreferencesView, TicketView, LogoutView,
    save_preferences_answers, AfterCreatedCredentialView, CustomerCredential,
    login_access, EventTransmissionView)

app_name = 'landing'

urlpatterns = [
     path('', HomeView.as_view(), name='home'),
     path('evento/', EventsView.as_view(), name='event'),
     path('transmision/<slug>/', EventTransmissionView.as_view(), name='transmission'), # noqa
     path('logout/', LogoutView.as_view(), name='logout'),
     path('validate_register/', validate_register, name='validate_register'),
     path('confirm_register/', confirm_register, name='confirm_register'),
     path('login_access/', login_access, name='login_access'),
     path('generar-credencial/',
          GenerateCredentialView.as_view(), name='generate_credential'),
     path('after-generated/<uid>/',
          AfterCreatedCredentialView.as_view(), name='credential_generated'),
     path('preferencias/',
          SelectPreferencesView.as_view(), name='select_preferences'),
     path('ticket/',
          TicketView.as_view(), name='ticket_view'),
     path('save_preferences_answers/', save_preferences_answers,
          name='save_preferences_answers'),
     path('download-credential-image/<uid>/',
          CustomerCredential.as_view(), name='download_credential'),
]
