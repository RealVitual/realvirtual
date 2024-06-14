from django.shortcuts import render
from src.apps.companies.models import HomePage
from django.views.generic import CreateView, View
from django.http import HttpResponse
from rest_framework.views import APIView
import requests
from src.apps.events.models import Event
from .models import (
    Video, Sponsor, CredentialCustomer, CredentialSettings, Question,
    UserAnswer, TicketSettings)
from .forms import (
    RegisterForm, CredentialCustomerForm, LoginForm)
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from .utils import record_to_pdf
from src.apps.tickets.utils import generate_ticket_code
from storages.backends.s3boto3 import S3Boto3Storage


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
        if request.company:
            company = request.company
            home_page = HomePage.objects.get(company=company)
            events = Event.objects.filter(
                is_active=True, company=company).order_by('start_datetime')
            videos = Video.objects.filter(
                is_active=True, company=company).order_by('position')
            sponsors = Sponsor.objects.filter(
                is_active=True, company=company).order_by('position')
            context = {
                'header': True,
                'form_register': self.get_form(),
                'form_login': LoginForm(initial=dict(company=request.company)),
                'events': events,
                'home_page': home_page,
                'videos': videos,
                'sponsors': sponsors
            }
        return render(request, self.template_name, context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def validate_register(request):
    if request.method == 'POST' and is_ajax(request=request):
        data = request.POST.dict()
        register_form = RegisterForm(
            initial=dict(domain=request.META['HTTP_HOST'],
                         company=request.company),
            data=data,
            prefix="register"
            )
        response_data = {}
        if register_form.is_valid():
            response_data['success'] = 1
            response_data['message'] = 'OK'
            form_object = register_form.save()
            user = form_object.get('user', None)
            if user:
                login(request, user)
                url = "generate_credential"
                if user.in_person:
                    company = request.company
                    company.current_quantity += 1
                    company.save()
                    company.refresh_from_db()
                    url = "select_preferences"
                response_data['success'] = 1
                response_data['redirect_url'] = reverse('landing:%s' % url)
        else:
            response_data['success'] = 0
            response_data['message'] = register_form.errors['message'].as_data()[0].args[0] # noqa
            response_data['can_confirm'] = register_form.errors['can_confirm'].as_data()[0].args[0] # noqa
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
            print(form_object, 'FORM OBJECT')
            user = form_object.get('user', None)
            if user:
                login(request, user)
                url = "generate_credential"
                if user.in_person:
                    company = request.company
                    company.current_quantity += 1
                    company.save()
                    company.refresh_from_db()
                    url = "select_preferences"
                response_data['success'] = 1
                response_data['redirect_url'] = reverse('landing:%s' % url)
        else:
            print(register_form.errors, '<-- ERRORS')
            response_data['success'] = 0
            response_data['message'] = register_form.errors['message'].as_data()[0].args[0] # noqa
            response_data['can_confirm'] = register_form.errors['can_confirm'].as_data()[0].args[0] # noqa
        print(response_data, 'RESPONSE DATA')
        return HttpResponse(
            json.dumps(response_data), content_type="application/json")


class EventsView(View):
    template_name = "landing/eventos-listado.html"

    def get(self, request, **kwargs):
        events = []
        # if request.company:
        #     company = request.company
        #     events = Event.objects.filter(
        #         is_active=True, company=company).order_by('position')
        context = {
            'header': True,
            # 'events': events,
        }
        return render(request, self.template_name, context)


class SelectPreferencesView(View):
    template_name = "landing/ayudanos.html"

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


# class TicketView(View):
#     template_name = "landing/ticket.html"

#     def get(self, request, **kwargs):
#         context = {
#         }
#         return render(request, self.template_name, context)


class TicketView(View):
    template_name = "landing/ticket_view.html"
    user = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('landing:home'))
        self.user = request.user
        return super(TicketView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        tickets = self.user.user_tickets.filter(company=request.company)
        if not tickets:
            return redirect(reverse('landing:home'))
        ticket = tickets.last()
        ticket_settings, created = TicketSettings.objects.get_or_create(
            company=request.company)
        context = {
            'header': False,
            'ticket': ticket,
            'settings': ticket_settings,
            'names': self.user.full_name,
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

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if not self.user.is_authenticated:
            return redirect(reverse('landing:home'))
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
        login_form = LoginForm(
            initial=dict(company=request.company),
            data=data)
        response_data = {}

        if login_form.is_valid():
            form_object = login_form.save()
            user = form_object.get('user', None)
            user_access = form_object.get('user_access')
            if user_access:
                login(request, user)
                if user.in_person:
                    url = "select_preferences"
                    if user.user_tickets.filter(company=request.company):
                        url = "event"
                else:
                    url = "generate_credential"
                    if user.credentials.filter(company=request.company):
                        url = "event"
            response_data['redirect_url'] = reverse('landing:%s' % url)
            response_data['success'] = 1
            response_data['message'] = 'Acceso exitoso'
        else:
            response_data['success'] = 0
            response_data['message'] = 'Error de acceso'

        return HttpResponse(
            json.dumps(response_data), content_type="application/json")
