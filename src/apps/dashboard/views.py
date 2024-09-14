from django.views.generic import CreateView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from src.apps.events.models import Event, ScheduleCustomerEvent, CustomerEvent
from src.apps.customers.models import Customer
from django.contrib import messages
from django.db.models import Count
from datetime import datetime
from src.apps.users.models import User


class DashboardView(View):
    user = None
    customer = None
    form = None
    template_name = "admin/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if not self.user.is_authenticated:
            return redirect(reverse('dashboard:login'))
        if not self.user.is_superuser:
            logout(request)
            return redirect(reverse(
                'dashboard:login'))
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        now = datetime.now()
        events = Event.objects.filter(
            is_active=True
        ).order_by('name')
        customers = User.objects.exclude(is_superuser=True).order_by('-created')
        schedules = ScheduleCustomerEvent.objects.select_related(
            'event')
        quantity_scheduled_events = schedules.values_list(
            'event', flat=True).distinct().count()
        events_quantity = events.count()
        no_scheduled_events = events_quantity - quantity_scheduled_events
        no_scheduled_events = no_scheduled_events if no_scheduled_events >= 0 else 0
        events = events.annotate(num_schedules=Count('event_schedules'))
        schduled_quantity = schedules.count()
        context = {
            "events": events,
            "schduled_quantity": schduled_quantity,
            "customers": customers[:10] if customers.count() >= 10 else customers,
            "customers_number": customers.count(),
            "no_scheduled_events": no_scheduled_events,
            "asistants": CustomerEvent.objects.count(),
            'day': now.strftime("%d"),
            'month': now.strftime("%m"),
            'current': now.strftime("%I:%M %p")
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
            'form': LoginForm(),
           }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.object = None
        data = request.POST
        form = LoginForm(data)
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
