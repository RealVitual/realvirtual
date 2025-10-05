from django.views.generic import CreateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from src.apps.events.models import (
    Event, ScheduleCustomerEvent, CustomerEvent,
    ScheduleCustomerWorkshop,
)
from src.apps.customers.models import Customer
from django.contrib import messages
from django.db.models import Count
from datetime import datetime
from src.apps.users.models import User
from src.apps.companies.models import UserCompany, Header


class DashboardView(View):
    user = None
    customer = None
    form = None
    template_name = "admin/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if not self.user.is_authenticated:
            return redirect(reverse('dashboard:login'))
        company_users = UserCompany.objects.filter(
            user=self.user, company=request.company)
        if not company_users:
            return redirect(reverse('dashboard:login'))
        if self.user.is_superuser or company_users.last().is_admin:
            pass
        else:
            return redirect(reverse(
                'landing:home'))
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        events = Event.objects.filter(
            is_active=True
        ).order_by('name')
        customers = UserCompany.objects.filter(
            company=request.company).exclude(
                is_admin=True).order_by('-user__modified')
        header = Header.objects.get(
            company=request.company
        )
        workshop_schedules = ScheduleCustomerWorkshop.objects.filter(
            company=request.company
        )
        scheduled_events = ScheduleCustomerEvent.objects.filter(
            company=request.company
        )
        context = {
            "events": events,
            "customers": customers[:10] if customers.count() >= 10 else customers,
            "customers_number": customers.count(),
            "asistants": CustomerEvent.objects.filter(
                company_user__company=request.company).count(),
            'day': now.strftime("%d"),
            'month': now.strftime("%m"),
            'current': now.strftime("%I:%M %p"),
            'header': header,
            'workshop_schedules': workshop_schedules,
            'workshop_schedules_number': workshop_schedules.count(),
            'scheduled_events': scheduled_events,
            'scheduled_events_number': scheduled_events.count()
           }
        return render(request, self.template_name, context)


class LoginView(View):
    user = None
    form_class = LoginForm
    customer = None
    form = None
    template_name = "admin/auth.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if self.user.is_authenticated:
            return redirect(reverse('dashboard:dashboard'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'form': LoginForm(initial=dict(company=request.company)),
           }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.object = None
        data = request.POST
        form = LoginForm(data, initial=dict(company=request.company))
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            print(form.errors)
            return self.form_invalid(form, request)

    def form_valid(self, form, request):
        self.object = form.save()
        user = self.object
        login(request, user)
        return redirect(reverse(
            'dashboard:dashboard'))

    def form_invalid(self, form, request):
        messages.error(
                request, form.non_field_errors())
        return redirect(reverse(
            'dashboard:login'))


class LogoutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return redirect(reverse(
            'dashboard:login'))
