import pytz
from django.utils.safestring import mark_safe
from src.apps.companies.models import HomePage
from django.views.generic import CreateView, View
from django.http import HttpResponse
from rest_framework.views import APIView
import requests
from src.apps.companies.models import UserCompany
from src.apps.events.models import (
    Event, Exhibitor, Filter, Schedule, Shift, ScheduleCustomerEvent,
    CustomerEvent)
from .models import (
    Video, Sponsor, CredentialCustomer, CredentialSettings, Question,
    UserAnswer, TicketSettings, SurveryQuestion, UserSurveyAnswer,
    NetworkingOption, UserNetworkingPreference)
from .forms import (
    RegisterForm, CredentialCustomerForm, LoginForm, EmailPasswordForm,
    ResetPasswordForm)
from django.contrib.auth import login, logout
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from datetime import datetime
from .utils import record_to_pdf
from src.apps.tickets.utils import generate_ticket_code
from django.conf import settings
from src.apps.users.permissions import (
    AuthenticatedPermission, )
from django.db.models import Q


class HomeView(CreateView):
    template_name = "landing/home.html"
    form_class = RegisterForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(
            HomeView, self).get_form_kwargs(**kwargs)
        form_kwargs["initial"] = dict(
            domain=self.request.META['HTTP_HOST'],
            company=self.request.company)
        form_kwargs["prefix"] = "register"
        return form_kwargs

    def get(self, request, **kwargs):
        context = {}
        months = {
            "January": "Enero", "February": "Febrero",
            "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio",
            "August": "Agosto", "September": "Setiembre",
            "October": "Octubre", "November": "Noviembre",
            "December": "Diciembre"
        }
        if request.company:
            company = request.company
            home_page = HomePage.objects.get(company=company)
            filtered_date = None
            query_filters = dict(request.GET)
            filtered_categories = []
            filtered_filters = []
            filtered_shift = None
            schedules = []
            for filter, value in query_filters.items():
                if 'fbclid' not in filter:
                    if filter == "date":
                        filtered_date = value[0]
                    elif filter == "shift":
                        filtered_shift = value[0]
                    else:
                        filtered_filters.append(filter)
                        filtered_categories.append(value[0])
            schedules_query = Schedule.objects.filter(
                event__is_active=True,
                event__company=company,
                is_active=True).order_by(
                    'event__start_datetime', 'start_time')
            events_list = list(dict.fromkeys(
                [schedule.event for schedule in schedules_query]))
            shifts = list(dict.fromkeys(
                [schedule.shift for schedule in schedules_query]))
            dates = [event.start_datetime for event in events_list]
            if filtered_categories:
                schedules_query = schedules_query.filter(
                    categories__filter_name__in=filtered_categories).order_by(
                        'event__start_datetime', 'start_time')
            events_list = list(dict.fromkeys(
                [schedule.event for schedule in schedules_query]))
            if filtered_date:
                events_list = [event for event in events_list if event.get_date() == filtered_date] # noqa
                schedules_query = schedules_query.filter(event__in=events_list)
            if filtered_shift:
                schedules_query = schedules_query.filter(
                    shift__filter_name=filtered_shift)
                filtered_shift = Shift.objects.get(filter_name=filtered_shift)
            for schedule in schedules_query:
                if schedule not in schedules:
                    schedules.append(schedule)
            dates_select = []
            for date in dates:
                option_date = date.astimezone(pytz.timezone(
                    settings.TIME_ZONE))
                month = months.get(date.strftime("%B"))
                dates_select.append(
                    option_date.strftime("%d de {}".format(month)))
            videos = Video.objects.filter(
                is_active=True, company=company).order_by('position')
            sponsors = Sponsor.objects.filter(
                is_active=True, company=company).order_by('position')
            filters = []
            if company.use_filters:
                filters = Filter.objects.filter(
                    company=request.company, is_active=True
                ).order_by('position')
            context = {
                'company': company,
                'header': True,
                'form_register': self.get_form(),
                'form_login': LoginForm(initial=dict(company=request.company)),
                'schedules': schedules,
                'home_page': home_page,
                'videos': videos,
                'sponsors': sponsors,
                'dates_select': dates_select,
                'filtered_date': filtered_date if filtered_date else None,
                'exhibitors': Exhibitor.objects.filter(
                    company=company, is_active=True),
                'filters': filters,
                'filtered_categories': filtered_categories,
                'filtered_filters': filtered_filters,
                'shifts':  shifts,
                'filtered_shift': filtered_shift.name if filtered_shift else None
            }
        return render(request, self.template_name, context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def validate_register(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        recaptcha_response = data.pop('g-recaptcha-response')
        access_type = data.pop('access_type', None)
        recaptcha_data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data=recaptcha_data)
        result = r.json()
        response_data = {}
        if result['success'] or request.session.get('used_recaptcha', None):
            request.session['used_recaptcha'] = 1
            register_form = RegisterForm(
                initial=dict(domain=request.META['HTTP_HOST'],
                             company=request.company,
                             access_type=access_type),
                data=data,
                prefix="register"
                )
            if register_form.is_valid():
                response_data['success'] = 1
                response_data['message'] = 'OK'
                form_object = register_form.save()
                user = form_object.get('user', None)
                user_company = form_object.get('user_company', None)
                if user:
                    login(request, user)
                    url = 'event'
                    if request.company.enable_credentials:
                        url = "generate_credential"
                    if user_company.in_person:
                        company = request.company
                        company.current_quantity += 1
                        company.save()
                        company.refresh_from_db()
                        url = "select_preferences"
                        if not request.company.enable_preferences:
                            generate_ticket_code(user, request.company)
                            record_to_pdf(
                                user, domain=request.build_absolute_uri('/')[:-1], # noqa
                                company=request.company)
                            url = "ticket_view"
                    response_data['success'] = 1
                    response_data['confirmed'] = user_company.confirmed
                    response_data['confirmed_message'] = request.company.message_confirm_user # noqa
                    response_data['redirect_url'] = reverse('landing:%s' % url)
                del request.session['used_recaptcha']
            else:
                print(register_form.errors)
                response_data['success'] = 0
                response_data['message'] = register_form.errors['message'].as_data()[0].args[0] # noqa
                response_data['can_confirm'] = register_form.errors['can_confirm'].as_data()[0].args[0] # noqa
        else:
            response_data['success'] = 0
            response_data['captcha_error'] = 1
            response_data['message'] = 'reCAPTCHA Inválido, Por favor inténtelo nuevamente.' # noqa
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


def confirm_register(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        print(data, 'DATA')
        register_form = RegisterForm(
            initial=dict(domain=request.META['HTTP_HOST'],
                         company=request.company,
                         is_confirmation=True),
            data=data,
            prefix="register"
            )
        response_data = {}
        if register_form.is_valid():
            form_object = register_form.save()
            user = form_object.get('user', None)
            user_company = form_object.get('user_company', None)
            if user:
                login(request, user)
                url = 'event'
                if request.company.enable_credentials:
                    url = "generate_credential"
                if user_company.in_person:
                    company = request.company
                    company.current_quantity += 1
                    company.save()
                    company.refresh_from_db()
                    url = "select_preferences"
                    if not request.company.enable_preferences:
                        generate_ticket_code(user, request.company)
                        record_to_pdf(
                            user, domain=request.build_absolute_uri('/')[:-1], # noqa
                            company=request.company)
                        url = "ticket_view"
                response_data['success'] = 1
                response_data['confirmed'] = user_company.confirmed
                response_data['redirect_url'] = reverse('landing:%s' % url)
                response_data['confirmed_message'] = request.company.message_confirm_user # noqa
        else:
            response_data['success'] = 0
            response_data['message'] = register_form.errors['message'].as_data()[0].args[0] # noqa
            response_data['can_confirm'] = register_form.errors['can_confirm'].as_data()[0].args[0] # noqa
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


class EventsView(CreateView):
    template_name = "landing/evento-detalle.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(EventsView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(
            EventsView, self).get_form_kwargs(**kwargs)
        form_kwargs["initial"] = dict(
            domain=self.request.META['HTTP_HOST'],
            company=self.request.company)
        form_kwargs["prefix"] = "register"
        return form_kwargs

    def get(self, request, **kwargs):
        context = {}
        months = {
            "January": "Enero", "February": "Febrero",
            "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio",
            "August": "Agosto", "September": "Setiembre",
            "October": "Octubre", "November": "Noviembre",
            "December": "Diciembre"
        }
        if request.company:
            company = request.company
            home_page = HomePage.objects.get(company=company)
            filtered_date = None
            query_filters = dict(request.GET)
            filtered_categories = []
            filtered_filters = []
            filtered_shift = None
            schedules = []
            for filter, value in query_filters.items():
                if 'fbclid' not in filter:
                    if filter == "date":
                        filtered_date = value[0]
                    elif filter == "shift":
                        filtered_shift = value[0]
                    else:
                        filtered_filters.append(filter)
                        filtered_categories.append(value[0])
            schedules_query = Schedule.objects.filter(
                event__is_active=True,
                event__company=company,
                is_active=True).order_by(
                    'event__start_datetime', 'start_time')
            events_list = list(dict.fromkeys(
                [schedule.event for schedule in schedules_query]))
            shifts = list(dict.fromkeys(
                [schedule.shift for schedule in schedules_query]))
            dates = [event.start_datetime for event in events_list]
            if filtered_categories:
                schedules_query = schedules_query.filter(
                    categories__filter_name__in=filtered_categories).order_by(
                        'event__start_datetime', 'start_time')
            events_list = list(dict.fromkeys(
                [schedule.event for schedule in schedules_query]))
            if filtered_date:
                events_list = [event for event in events_list if event.get_date() == filtered_date] # noqa
                schedules_query = schedules_query.filter(event__in=events_list)
            if filtered_shift:
                schedules_query = schedules_query.filter(shift__filter_name=filtered_shift)
                filtered_shift = Shift.objects.get(filter_name=filtered_shift)
            for schedule in schedules_query:
                if schedule not in schedules:
                    schedules.append(schedule)
            dates_select = []
            for date in dates:
                option_date = date.astimezone(pytz.timezone(
                    settings.TIME_ZONE))
                month = months.get(date.strftime("%B"))
                dates_select.append(
                    option_date.strftime("%d de {}".format(month)))
            videos = Video.objects.filter(
                is_active=True, company=company).order_by('position')
            sponsors = Sponsor.objects.filter(
                is_active=True, company=company).order_by('position')
            filters = []
            if company.use_filters:
                filters = Filter.objects.filter(
                    company=request.company, is_active=True
                ).order_by('position')
            context = {
                'company': company,
                'header': True,
                'form_register': self.get_form(),
                'form_login': LoginForm(initial=dict(company=request.company)),
                'schedules': schedules,
                'home_page': home_page,
                'videos': videos,
                'sponsors': sponsors,
                'dates_select': dates_select,
                'filtered_date': filtered_date if filtered_date else None,
                'exhibitors': Exhibitor.objects.filter(
                    company=company, is_active=True),
                'filters': filters,
                'filtered_categories': filtered_categories,
                'filtered_filters': filtered_filters,
                'shifts':  shifts,
                'filtered_shift': filtered_shift.name if filtered_shift else None
            }
        return render(request, self.template_name, context)


class SelectPreferencesView(View):
    template_name = "landing/ayudanos.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(SelectPreferencesView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, **kwargs):
        questions = Question.objects.filter(
            company=request.company, is_active=True).order_by('position')
        context = {
            "questions": questions,
            'header': False,
        }
        return render(request, self.template_name, context)


@login_required
def save_preferences_answers(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        print(data, 'DATA')
        user = request.user
        UserAnswer.objects.filter(user=user, company=request.company).delete()
        response_data = {}
        for key, value in data.items():
            print(key, value)
            answer = UserAnswer(user=user, company=request.company)
            answer.question_id = int(key)
            answer.choice_question_id = int(value)
            answer.save()
        url = "ticket_view"
        response_data['redirect_url'] = reverse('landing:%s' % url)
        generate_ticket_code(user, request.company)
        record_to_pdf(
            user, domain=request.build_absolute_uri('/')[:-1],
            company=request.company)
        response_data['success'] = 1
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


class TicketViewPDF(View):
    template_name = "landing/ticket.html"

    def get(self, request, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)


class TicketView(View):
    template_name = "landing/ticket_view.html"
    user = None

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        self.user_company = UserCompany.objects.get(
            company=company, user=request.user)
        if not self.user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(TicketView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        tickets = request.user.user_tickets.filter(company=request.company)
        if not tickets:
            return redirect(reverse('landing:home'))
        ticket = tickets.last()
        ticket_settings, created = TicketSettings.objects.get_or_create(
            company=request.company)
        context = {
            'header': False,
            'ticket': ticket,
            'settings': ticket_settings,
            'names': self.user_company.full_name,
            'domain': request.build_absolute_uri('/')[:-1]
        }
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return redirect(reverse(
            'landing:home'))


class GenerateCredentialView(CreateView):
    model = CredentialCustomer
    form_class = CredentialCustomerForm
    template_name = "landing/credencial.html"
    landing_page = None
    slug = None
    user = None

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        self.user = request.user
        user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not user_company.confirmed:
            return redirect(reverse('landing:home'))
        if not request.company.enable_credentials:
            return redirect(reverse('landing:event'))
        return super(GenerateCredentialView, self).dispatch(request, *args, **kwargs) # noqa

    def get(self, request, *args, **kwargs):
        credential_settings = CredentialSettings.objects.filter(
            company=request.company
        )
        context = {
            'header': False,
            'credential_settings': credential_settings[0] if credential_settings else None, # noqa
            'customer': self.user,
            'form': self.get_form(),
            }
        return render(request, self.template_name, context)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(
            GenerateCredentialView, self).get_form_kwargs(**kwargs)
        now = datetime.now()
        now_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        form_kwargs["initial"] = dict(
            date_name=now_string, user=self.user, company=self.request.company)
        return form_kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            print(form.errors)
            return self.form_invalid(form, request)

    def form_valid(self, form, request):
        self.object = form.save()
        form_object = self.object
        instance = form_object['credential']
        return redirect(reverse(
            'landing:credential_generated', kwargs=dict(uid=instance.code)))


class AfterCreatedCredentialView(View):
    template_name = "landing/credencial-generada.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not user_company.confirmed:
            return redirect(reverse('landing:home'))
        if not request.company.enable_credentials:
            return redirect(reverse('landing:event'))
        return super(AfterCreatedCredentialView, self).dispatch(request, *args, **kwargs) # noqa

    def get(self, request, **kwargs):
        code = self.kwargs['uid']
        credential_settings = CredentialSettings.objects.filter(
            company=request.company
        )
        instance = get_object_or_404(
            CredentialCustomer, code=code)
        url_share = request.META['HTTP_HOST'] + reverse(
                'landing:credential_generated', kwargs=dict(uid=instance.code))
        context = {
            'credential_settings': credential_settings[0] if credential_settings else None, # noqa
            "instance": instance,
            "url_share": url_share,
            'header': False,
        }
        return render(request, self.template_name, context)


class CustomerCredential(APIView):
    permission_classes = []

    def get(self, request, **kwargs):
        code = self.kwargs['uid']
        instance = get_object_or_404(
            CredentialCustomer, code=code)
        img = requests.get(instance.credential_img.url)
        response = HttpResponse(img.content, content_type='image/jpg')
        response['Content-Disposition'] = 'attachment; filename=%s' % instance.credential_img.name.split('/')[-1] # noqa
        return response


def login_access(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        recaptcha_response = data.pop('g-recaptcha-response')
        recaptcha_data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data=recaptcha_data)
        result = r.json()
        response_data = {}
        if result['success'] or request.session.get('used_recaptcha', None):
            request.session['used_recaptcha'] = 1
            login_form = LoginForm(
                initial=dict(company=request.company),
                data=data)
            if login_form.is_valid():
                form_object = login_form.save()
                user = form_object.get('user', None)
                user_access = form_object.get('user_access')
                if user_access:
                    login(request, user)
                    url = "event"
                    if user.in_person and request.company.enable_preferences:
                        url = "select_preferences"
                        if user.user_tickets.filter(company=request.company):
                            url = "event"
                    if user.virtual and request.company.enable_credentials:
                        url = "generate_credential"
                        if user.credentials.filter(company=request.company):
                            url = "event"
                response_data['redirect_url'] = reverse('landing:%s' % url)
                response_data['success'] = 1
                response_data['message'] = 'Acceso exitoso'
                del request.session['used_recaptcha']
            else:
                response_data['success'] = 0
                response_data['message'] = login_form.errors['message'].as_data()[0].args[0] # noqa
                print(response_data, 'RESPONSE DATA')
        else:
            response_data['success'] = 0
            response_data['captcha_error'] = 1
            response_data['message'] = 'reCAPTCHA Inválido, Por favor inténtelo nuevamente.' # noqa
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


class EventTransmissionView(View):
    template_name = "landing/chat.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        self.user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not self.user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(EventTransmissionView, self).dispatch(request, *args, **kwargs) # noqa

    def get(self, request, **kwargs):
        months = {
            "January": "Enero", "February": "Febrero",
            "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio",
            "August": "Agosto", "September": "Setiembre",
            "October": "Octubre", "November": "Noviembre",
            "December": "Diciembre"
        }
        hour_code = {
            "PM": "p.m.", "AM": "a.m."
        }
        days = {
            "Sunday": "Domingo", "Monday": "Lunes",
            "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes",
            "Saturday": "Sábado"
        }
        event = []
        context = dict()
        slug = self.kwargs['slug']
        if request.company:
            company = request.company
            event = Event.objects.get(
                slug=slug, company=company)
            date = event.start_datetime.astimezone(pytz.timezone(settings.TIME_ZONE)) # noqa
            end_date = event.end_datetime.astimezone(pytz.timezone(settings.TIME_ZONE)) # noqa
            month = months.get(date.strftime("%B"))
            day = days.get(date.strftime("%A"))
            h_code = date.strftime("%p")
            end_h_code = end_date.strftime("%p")
            h_code = hour_code.get(h_code)
            end_h_code = hour_code.get(end_h_code)
            start_date = date.strftime("{} %d de {} %Y".format(day, month.lower())) # noqa
            start_time = date.strftime("%I:%M {}".format(h_code))
            end_time = end_date.strftime("%I:%M {}".format(end_h_code))
            CustomerEvent.objects.get_or_create(event=event, company_user=self.user_company)
            context = {
                'start_date': start_date,
                'start_time': start_time,
                'end_time': end_time,
                'company': company,
                'event': event,
                'chat_url': settings.CHAT_URL.split('/')[-1],
                'room_name_json': mark_safe(json.dumps(
                    event.chat_code)),
                'room_id': mark_safe(json.dumps(event.chat_id)),
            }
        return render(request, self.template_name, context)


class CustomerTicket(APIView):
    permission_classes = [AuthenticatedPermission]

    def get(self, request, **kwargs):
        tickets = request.user.user_tickets.filter(company=request.company)
        if not tickets:
            return redirect(reverse('landing:home'))
        ticket = tickets.last()
        img = requests.get(ticket.pdf.url)
        response = HttpResponse(img.content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % \
            ticket.pdf.name.split('/')[-1]
        return response


class SurveyView(View):
    template_name = "landing/encuesta.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(SurveyView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        questions = SurveryQuestion.objects.filter(
            company=request.company, is_active=True).order_by('position')
        context = {
            "questions": questions,
            'header': False,
        }
        return render(request, self.template_name, context)


class SuccessSurveyView(View):
    template_name = "landing/encuesta-gracias.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(SuccessSurveyView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, **kwargs):
        home_page = HomePage.objects.get(company=request.company)
        context = {
            "home_page": home_page
        }
        return render(request, self.template_name, context)


@login_required
def save_survey_answers(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        user = request.user
        UserSurveyAnswer.objects.filter(
            user=user, company=request.company).delete()
        response_data = {}
        for key, value in data.items():
            print(key, 'KEY!')
            print(value, 'VALUE!')
            answer = UserSurveyAnswer(
                user=user, company=request.company)
            answer.question_id = int(key)
            answer.choice_question_id = int(value)
            answer.save()
        url = "finished_survey"
        response_data['redirect_url'] = reverse('landing:%s' % url)
        response_data['success'] = 1
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


class NetworkingView(View):
    template_name = "landing/networking.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        self.user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not self.user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(NetworkingView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        options = NetworkingOption.objects.filter(
            company=request.company, is_active=True).order_by('name')
        preferences = UserNetworkingPreference.objects.filter(
            user_company=self.user_company, company=request.company
        ).values_list('networking_option__id', flat=True)
        home_page = HomePage.objects.get(company=request.company)
        context = {
            "options": options,
            'header': False,
            'preferences': preferences,
            "home_page": home_page
        }
        return render(request, self.template_name, context)


@login_required
def allow_networking_user(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        user = request.user
        networking = int(data.get('networking', 1))
        company_user = UserCompany.objects.get(user=request.user,
                                               company=request.company)
        user.allow_networking = networking
        company_user.allow_networking = networking
        company_user.save()
        user.save()
        response_data = {}
        url = "networking_preferences"
        if not networking:
            url = "home"
        response_data['redirect_url'] = reverse('landing:%s' % url)
        response_data['success'] = 1
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


@login_required
def save_networking_preferences(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        user = request.user
        user_company = UserCompany.objects.get(
            company=request.company, user=user)
        UserNetworkingPreference.objects.filter(
            user_company=user_company, company=request.company
        ).delete()
        for key, value in data.items():
            answer = UserNetworkingPreference(
                user_company=user_company, company=request.company)
            answer.networking_option_id = int(key)
            answer.save()

        response_data = {}
        url = "networking"
        response_data['redirect_url'] = reverse('landing:%s' % url)
        response_data['success'] = 1
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


class NetworkingUsersView(View):
    template_name = "landing/networking-si-continuar.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        self.user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not self.user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(NetworkingUsersView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, **kwargs):
        networking_users = UserCompany.objects.filter(
            company=request.company, allow_networking=True
        ).exclude(email=self.user_company.email)
        networking_preferences = UserNetworkingPreference.objects.filter(
            company=request.company, user_company__allow_networking=True
        ).exclude(user_company=self.user_company)
        options_id = networking_preferences.values_list(
            'networking_option__id', flat=True)
        selected_category = None
        search_query = ""
        query_filters = dict(request.GET)
        for filter, value in query_filters.items():
            if filter == "category":
                selected_category = value[0]
                networking_preferences = networking_preferences.filter(
                    networking_option=selected_category
                )
                user_companies_id = networking_preferences.values_list('user_company__id', flat=True)
                networking_users = networking_users.filter(id__in=user_companies_id)
            if filter == "search":
                networking_users = networking_users.filter(
                    Q(full_name__icontains=value[0]) |
                    Q(job_company_select__name__icontains=value[0]) |
                    Q(job_company__icontains=value[0]) |
                    Q(company_position__icontains=value[0])
                )
                search_query = value[0]

        options = ['']
        options = NetworkingOption.objects.filter(
            company=request.company,
            is_active=True, id__in=options_id).order_by('name')
        home_page = HomePage.objects.get(company=request.company)
        context = {
            "networking_users": networking_users,
            "options": options,
            "home_page": home_page,
            "selected_category": int(selected_category) if selected_category else None,
            "search_query": search_query
        }
        return render(request, self.template_name, context)


class RecoverPasswordView(CreateView):
    form_class = EmailPasswordForm
    template_name = "landing/olvido-contrasena.html"
    landing_page = None
    slug = None

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(
            RecoverPasswordView, self).get_form_kwargs(**kwargs)
        form_kwargs["initial"] = dict(
            domain=self.request.build_absolute_uri('/')[:-1],
            company=self.request.company)
        return form_kwargs

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('landing:generate_credential'))
        context = {
            'form': self.get_form()
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)

    def form_valid(self, form, request):
        form.save()
        messages.info(request, "Se ha enviado un correo con instrucciones")
        return redirect(reverse(
                    'landing:recover_password'))

    def form_invalid(self, form, request):
        messages.error(
                request, form.non_field_errors())
        return redirect(reverse(
            'landing:recover_password'))


class ScheduledEventsView(View):
    template_name = "landing/eventos-agendados.html"

    def dispatch(self, request, *args, **kwargs):
        company = self.request.company
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        user_company = UserCompany.objects.get(company=company,
                                               user=request.user)
        if not user_company.confirmed:
            return redirect(reverse('landing:home'))
        return super(ScheduledEventsView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, **kwargs):
        context = {}
        months = {
            "January": "Enero", "February": "Febrero",
            "March": "Marzo", "April": "Abril",
            "May": "Mayo", "June": "Junio", "July": "Julio",
            "August": "Agosto", "September": "Setiembre",
            "October": "Octubre", "November": "Noviembre",
            "December": "Diciembre"
        }
        if request.company:
            company = request.company
            home_page = HomePage.objects.get(company=company)
            filtered_date = None
            query_filters = dict(request.GET)
            filtered_categories = []
            filtered_filters = []
            filtered_shift = None
            schedules = []
            for filter, value in query_filters.items():
                if filter == "date":
                    filtered_date = value[0]
                elif filter == "shift":
                    filtered_shift = value[0]
                else:
                    filtered_filters.append(filter)
                    filtered_categories.append(value[0])
            user_schedules = ScheduleCustomerEvent.objects.filter(
                company=request.company, user=request.user).values_list(
                    'schedule__id', flat=True)
            schedules_query = Schedule.objects.filter(
                event__is_active=True,
                event__company=company,
                id__in=user_schedules,
                is_active=True).order_by(
                    'event__start_datetime', 'start_time')
            events_list = list(dict.fromkeys(
                [schedule.event for schedule in schedules_query]))
            shifts = list(dict.fromkeys(
                [schedule.shift for schedule in schedules_query]))
            dates = [event.start_datetime for event in events_list]
            if filtered_categories:
                schedules_query = schedules_query.filter(
                    categories__filter_name__in=filtered_categories).order_by(
                        'event__start_datetime', 'start_time')
            events_list = list(dict.fromkeys(
                [schedule.event for schedule in schedules_query]))
            if filtered_date:
                events_list = [event for event in events_list if event.get_date() == filtered_date] # noqa
                schedules_query = schedules_query.filter(event__in=events_list)
            if filtered_shift:
                schedules_query = schedules_query.filter(shift__filter_name=filtered_shift)
                filtered_shift = Shift.objects.get(filter_name=filtered_shift)
            for schedule in schedules_query:
                if schedule not in schedules:
                    schedules.append(schedule)
            dates_select = []
            for date in dates:
                option_date = date.astimezone(pytz.timezone(
                    settings.TIME_ZONE))
                month = months.get(date.strftime("%B"))
                dates_select.append(
                    option_date.strftime("%d de {}".format(month)))
            videos = Video.objects.filter(
                is_active=True, company=company).order_by('position')
            sponsors = Sponsor.objects.filter(
                is_active=True, company=company).order_by('position')
            filters = []
            if company.use_filters:
                filters = Filter.objects.filter(
                    company=request.company, is_active=True
                ).order_by('position')
            context = {
                'company': company,
                'header': True,
                'schedules': schedules,
                'home_page': home_page,
                'videos': videos,
                'sponsors': sponsors,
                'dates_select': dates_select,
                'filtered_date': filtered_date if filtered_date else None,
                'exhibitors': Exhibitor.objects.filter(
                    company=company, is_active=True),
                'filters': filters,
                'filtered_categories': filtered_categories,
                'filtered_filters': filtered_filters,
                'shifts':  shifts,
                'filtered_shift': filtered_shift.name if filtered_shift else None
            }
        return render(request, self.template_name, context)


class ResetPasswordView(CreateView):
    form_class = ResetPasswordForm
    template_name = "landing/reset-password.html"
    uuid = None
    user = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        self.uuid = self.kwargs['uuid']
        self.user = get_object_or_404(
            UserCompany, uuid_hash=self.uuid)
        return super(ResetPasswordView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(
            ResetPasswordView, self).get_form_kwargs(**kwargs)
        form_kwargs["initial"] = dict(user=self.user)
        return form_kwargs

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.get_form()
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)

    def form_valid(self, form, request):
        form.save()
        return redirect(reverse('landing:home'))


class CertificateView(View):
    template_name = "landing/certificate.html"
    user = None

    def get(self, request, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)
