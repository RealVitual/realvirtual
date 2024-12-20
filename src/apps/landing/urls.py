from django.urls import path
from .views import (
    HomeView, EventsView, GenerateCredentialView, validate_register,
    confirm_register, SelectPreferencesView, TicketView, LogoutView,
    save_preferences_answers, AfterCreatedCredentialView, CustomerCredential,
    login_access, EventTransmissionView, CustomerTicket, SuccessSurveyView,
    SurveyView, save_survey_answers, allow_networking_user, NetworkingView,
    save_networking_preferences, NetworkingUsersView, RecoverPasswordView,
    ScheduledEventsView, TicketViewPDF, ResetPasswordView, CertificateView,
    CloseLandingView, GenerateCertificateView)

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
     path('download-customer-ticket/', CustomerTicket.as_view(),
          name='download_customer_ticket'),
     path('encuesta/',
          SurveyView.as_view(), name='survey_view'),
     path('encuesta-culminada/',
          SuccessSurveyView.as_view(), name='finished_survey'),
     path('save_survey_answers/', save_survey_answers,
          name='save_survey_answers'),
     path('allow_networking_user/', allow_networking_user,
          name='allow_networking_user'),
     path('networking-preferencias/', NetworkingView.as_view(),
          name='networking_preferences'),
     path('save_networking_preferences/', save_networking_preferences,
          name='save_networking_preferences'),
     path('networking/', NetworkingUsersView.as_view(),
          name='networking'),
     path('recover-password/',
          RecoverPasswordView.as_view(), name="recover_password"),
     path('agendados/',
          ScheduledEventsView.as_view(), name='scheduled_events'),
     path('reset-password/<uuid>/',
          ResetPasswordView.as_view(), name="reset_password"),
     # path('ticket-pdf/',
     #      TicketViewPDF.as_view(), name='ticket_view_pdf'),
     path('certificate/',
          CertificateView.as_view(), name='certificate'),
     path('fin/', CloseLandingView.as_view(), name='closed'),
     path('generar-certificado/',
          GenerateCertificateView.as_view(), name="generate_certificate"),
]
