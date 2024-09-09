from rest_framework import serializers
from src.apps.users.models import User
from src.apps.events.models import Schedule, ScheduleCustomerEvent
from src.apps.companies.models import EmailTemplate, EmailSettings
from django.template import Context, Template
from django.core.mail import EmailMessage
import threading
from django.conf import settings
from django.core.mail import get_connection


def send_html_mail(subject, html_content, e_mail, receptors,
                   a_file, customer, company):
    EmailThread(
        subject, html_content, e_mail, receptors,
        a_file, customer, company).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content,
                 e_mail, receptors, a_file, customer, company):
        self.subject = subject
        self.e_mail = e_mail
        self.html_content = html_content
        self.receptors = receptors
        self.a_file = a_file
        self.customer = customer
        self.company = company
        threading.Thread.__init__(self)

    def run(self):
        rules_email, created = EmailSettings.objects.get_or_create(
            company=self.company)
        print(rules_email.username, 'rules_email.username')
        print(rules_email.host, 'rules_email.host')
        # connection = get_connection(
        #     host=rules_email.host,
        #     port=rules_email.port,
        #     username=rules_email.username,
        #     password=rules_email.password,
        #     use_tls=rules_email.use_tls
        # )
        # connection.open()
        # msg = EmailMessage(
        #     self.subject, self.html_content, self.e_mail, self.receptors,
        #     connection)
        # msg.content_subtype = "html"

        if self.a_file:
            print(self.a_file, 'A FILE')
            # msg = EmailMessage(
            #     subject=self.subject,
            #     body=self.html_content,
            #     from_email=rules_email.username,
            #     to=self.receptors,
            #     connection=connection)
            msg = EmailMessage(
                subject=self.subject,
                body=self.html_content,
                from_email=rules_email.username,
                to=self.receptors)
            msg.content_subtype = "html"
            msg.attach(self.a_file[1], self.a_file[0], self.a_file[2])
            msg.send()
        # settings.EMAIL_HOST = rules_email.host
        # settings.EMAIL_PORT = rules_email.port
        # settings.EMAIL_HOST_USER = rules_email.username
        # settings.EMAIL_HOST_PASSWORD = rules_email.password
        # settings.EMAIL_USE_TLS = rules_email.use_tls

        # connection.close()
        print('SE ENVIÓ CORREO EXITOSAMENTE PARA ==>' + self.receptors[0])
        # if "Regi" in self.subject:
        #     User.objects.filter(email=self.receptors[0]).update(
        #         received_welcome_email=True)
        #     print('CLIENTE ACTUALIZADO!')


class GenerateCustomerScheduleSerializer(serializers.Serializer):
    schedule_id = serializers.CharField()
    status = serializers.IntegerField()

    def create(self, validated_data):
        user = self.context.get("user")
        company = self.context.get("company")
        status = self.validated_data.get("status")
        schedule_id = self.validated_data.get("schedule_id")
        schedule = Schedule.objects.get(id=int(schedule_id))
        if status:
            queryset = ScheduleCustomerEvent.objects.filter(
                schedule_id=schedule_id, user=user,
                event_id=schedule.event.id,
                company=company
            )
            if not queryset:
                ScheduleCustomerEvent.objects.create(
                    schedule_id=schedule_id, user=user,
                    event_id=schedule.event.id,
                    company=company
                )

        # Send email
            mailing = EmailTemplate.objects.get(company=company,
                                                email_type="SCHEDULE")
            if mailing.from_email:
                schedule = Schedule.objects.get(id=schedule_id)
                context = dict()
                context["names"] = user.names
                context["first_name"] = user.names.split(" ")[0]
                context["email"] = user.email
                context["schedule"] = schedule
                a_file = schedule.ics_file.read(), "event.ics", "text/calendar"

                mailing = EmailTemplate.objects.get(company=company,
                                                    email_type="SCHEDULE")
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
                    a_file, user, company)
        else:
            ScheduleCustomerEvent.objects.filter(
                schedule_id=schedule_id, user=user,
                event_id=schedule.event.id,
                company=company
            ).delete()

        return dict(success=True)
