from rest_framework import serializers
from src.apps.users.models import User
from src.apps.events.models import (
    Schedule, ScheduleCustomerEvent,
    Workshop, ScheduleCustomerWorkshop)
from src.apps.companies.models import EmailTemplate, EmailSettings, UserCompany
from django.template import Context, Template
from django.core.mail import EmailMessage
import threading
from django.conf import settings
from django.core.mail import get_connection


def send_html_mail(subject, html_content, e_mail, receptors,
                   a_file, customer, company, send_ics):
    EmailThread(
        subject, html_content, e_mail, receptors,
        a_file, customer, company, send_ics).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content,
                 e_mail, receptors, a_file, customer, company, send_ics):
        self.subject = subject
        self.e_mail = e_mail
        self.html_content = html_content
        self.receptors = receptors
        self.a_file = a_file
        self.customer = customer
        self.company = company
        self.send_ics = send_ics
        threading.Thread.__init__(self)

    def run(self):
        rules_email, created = EmailSettings.objects.get_or_create(
            company=self.company)
        connection = get_connection(
            host=rules_email.host,
            port=rules_email.port,
            username=rules_email.username,
            password=rules_email.password,
            use_tls=rules_email.use_tls
        )
        # connection.open()
        msg = EmailMessage(
            subject=self.subject,
            body=self.html_content,
            from_email=rules_email.username,
            to=self.receptors,
            connection=connection)
        msg.content_subtype = "html"

        if self.a_file and self.send_ics:
            print(self.a_file, 'A FILE')
            msg = EmailMessage(
                subject=self.subject,
                body=self.html_content,
                from_email=rules_email.username,
                to=self.receptors,
                connection=connection)
            msg.content_subtype = "html"
            msg.attach(self.a_file[1], self.a_file[0], self.a_file[2])
        msg.send()
        # connection.close()
        print('SE ENVIÓ CORREO EXITOSAMENTE PARA ==>' + self.receptors[0])


def send_schedule_event_mail(company_user, schedule_id, company):
    EmailScheduleThread(company_user, schedule_id, company).start()


class EmailScheduleThread(threading.Thread):
    def __init__(self, company_user, schedule_id, company):
        self.company_user = company_user
        self.schedule_id = schedule_id
        self.company = company
        threading.Thread.__init__(self)

    def run(self):
        mailings = EmailTemplate.objects.filter(
            company=self.company,
            email_type="SCHEDULE"
        )
        if mailings:
            mailing = mailings[0]
            schedule = Schedule.objects.get(id=self.schedule_id)
            context = dict()
            context["names"] = self.company_user.names
            context["first_name"] = self.company_user.names.split(" ")[0]
            context["email"] = self.company_user.email
            context["schedule"] = schedule
            a_file = schedule.ics_file.read(), "event.ics", "text/calendar"
            template = Template(mailing.html_code)
            html_content = template.render(Context(context))
            subject = mailing.subject
            receptors = [self.company_user.email]
            rules_email, created = EmailSettings.objects.get_or_create(
                company=self.company)
            connection = get_connection(
                host=rules_email.host,
                port=rules_email.port,
                username=rules_email.username,
                password=rules_email.password,
                use_tls=rules_email.use_tls
            )
            msg = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=rules_email.username,
                to=receptors,
                connection=connection)
            msg.content_subtype = "html"

            if a_file:
                msg = EmailMessage(
                    subject=subject,
                    body=html_content,
                    from_email=rules_email.username,
                    to=receptors,
                    connection=connection)
                msg.content_subtype = "html"
                msg.attach(a_file[1], a_file[0], a_file[2])
            msg.send()
            print('SE ENVIÓ CORREO EXITOSAMENTE PARA ==>' + receptors[0])


class GenerateCustomerScheduleSerializer(serializers.Serializer):
    schedule_id = serializers.CharField()
    status = serializers.IntegerField()

    def create(self, validated_data):
        user = self.context.get("user")
        company = self.context.get("company")
        status = self.validated_data.get("status")
        schedule_id = self.validated_data.get("schedule_id")
        schedule = Schedule.objects.get(id=int(schedule_id))
        company_user = UserCompany.objects.get(
            company=company, user=user
        )
        print(company_user)
        if status:
            queryset = ScheduleCustomerEvent.objects.filter(
                schedule_id=schedule_id, company_user=company_user,
                event_id=schedule.event.id,
                company=company
            )
            if not queryset:
                ScheduleCustomerEvent.objects.create(
                    schedule_id=schedule_id, company_user=company_user,
                    event_id=schedule.event.id,
                    company=company
                )

        # Send email
            send_schedule_event_mail(
                company_user, schedule_id, company
            )
        else:
            ScheduleCustomerEvent.objects.filter(
                schedule_id=schedule_id, company_user=company_user,
                event_id=schedule.event.id,
                company=company
            ).delete()

        return dict(success=True)


class GenerateCustomerWorkshopSerializer(serializers.Serializer):
    workshop_id = serializers.CharField()
    status = serializers.IntegerField()
    confirm = serializers.BooleanField()

    def create(self, validated_data):
        user = self.context.get("user")
        company = self.context.get("company")
        status = self.validated_data.get("status")
        confirm = self.validated_data.get("confirm")
        workshop_id = self.validated_data.get("workshop_id")
        workshop = Workshop.objects.get(id=int(workshop_id))
        print(confirm, 'CONFIRM!!')
        print(status, 'status!!')
        company_user = UserCompany.objects.get(
            company=company, user=user
        )
        # Validate is it confirmed
        # if not company_user.confirmed:
        #     return dict(success=False)

        # Validate workshop numbers
        _continue = self.check_validation(
            workshop, confirm
        )
        print(_continue, '_continue')
        send_ics = False
        if _continue:
            if status:
                queryset = ScheduleCustomerWorkshop.objects.filter(
                    workshop=workshop, company_user=company_user,
                    company=company
                )
                if not queryset:
                    ScheduleCustomerWorkshop.objects.create(
                        workshop=workshop, company_user=company_user,
                        company=company, confirmed=confirm
                    )
                if confirm:
                    send_ics = True
                    workshop.enrolled += 1
                    mailings = EmailTemplate.objects.filter(
                        company=company, email_type="WORKSHOP")
                else:
                    workshop.waiting_list_enrolled += 1
                    mailings = EmailTemplate.objects.filter(
                        company=company, email_type="WORKSHOP_WAITING")
                workshop.save()

                # Send email
                if mailings:
                    mailing = mailings[0]
                    context = dict()
                    context["names"] = company_user.names
                    context["first_name"] = company_user.names.split(" ")[0]
                    context["email"] = company_user.email
                    context["workshop"] = workshop
                    a_file = workshop.ics_file.read(), "event.ics", "text/calendar"
                    template = Template(mailing.html_code)
                    html_content = template.render(Context(context))
                    subject = mailing.subject
                    e_mail = u'{0}<{1}>'.format(
                        mailing.from_name, mailing.from_email)
                    msg = EmailMessage(
                        subject, html_content, e_mail, [user.email, ])
                    msg.content_subtype = "html"
                    print("ENVIAR CORREO ")
                    send_html_mail(
                        subject, html_content, e_mail, [user.email, ],
                        a_file, user, company, send_ics)
            else:
                ScheduleCustomerWorkshop.objects.filter(
                    workshop=workshop, company_user=company_user,
                    company=company
                ).delete()
            return dict(success=True, confirm=confirm)
        return dict(success=False, confirm=None)

    def check_validation(self, workshop, confirm) -> bool:
        if workshop.capacity > workshop.enrolled and confirm:
            return True
        if workshop.waiting_list_capacity:
            if workshop.waiting_list_capacity > workshop.waiting_list_enrolled and not confirm:
                return True
        return False
