from rest_framework import serializers
from src.apps.users.models import User
from src.apps.events.models import (
    Schedule, ScheduleCustomerEvent,
    Workshop, ScheduleCustomerWorkshop)
from src.apps.companies.models import (
    EmailTemplate, EmailSettings, UserCompany, Company)
from .models import Community, UserCommunityPreference
from django.template import Context, Template
from django.core.mail import EmailMessage
import threading
from django.core.mail import get_connection
from src.apps.tickets.utils import generate_ticket_code
from .utils import record_to_pdf


def send_html_mail(subject, context, html_code, e_mail, receptors,
                   customer, company, create_ticket, domain_pdf):
    EmailThread(
        subject, context, html_code, e_mail, receptors,
        customer, company, create_ticket, domain_pdf).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, context, html_code,
                 e_mail, receptors, customer, company,
                 create_ticket, domain_pdf):
        self.subject = subject
        self.e_mail = e_mail
        self.context = context
        self.html_code = html_code
        self.receptors = receptors
        self.customer = customer
        self.company = company
        self.create_ticket = create_ticket
        self.domain_pdf = domain_pdf
        threading.Thread.__init__(self)

    def run(self):
        if self.create_ticket:
            generate_ticket_code(self.customer.user, self.company)
            record_to_pdf(
                self.customer.user, domain=self.domain_pdf,
                company=self.company
            )
        tickets = self.customer.user.user_tickets.filter(company=self.company)
        url_ticket = ""
        if tickets:
            ticket = tickets.last()
            url_ticket = "%s/download_ticket/%s" % (
                self.domain_pdf, ticket.hash_id
            )
            self.context['url_ticket'] = url_ticket

        template = Template(self.html_code)
        html_content = template.render(Context(self.context))

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
            body=html_content,
            from_email=rules_email.username,
            to=self.receptors,
            connection=connection)
        msg.content_subtype = "html"
        msg.send()
        # connection.close()
        print('SE ENVIÓ CORREO EXITOSAMENTE PARA ==>' + self.receptors[0])


class ValidateInPersonCompanyUserSerializer(serializers.Serializer):
    status = serializers.BooleanField()

    def create(self, validated_data):
        user = self.context.get("user")
        company = self.context.get("company")
        domain_pdf = self.context.get("domain_pdf")
        status = self.validated_data.get("status")
        user_company = UserCompany.objects.get(
            company=company, user=user
        )
        message = ""
        create_ticket = False
        if status:
            create_ticket = True
            message = company.message_filter_found_domain_user
            user_company.in_person = True
            user_company.save()
            mailing, created = EmailTemplate.objects.get_or_create(
                company=company, email_type="TO_CONFIRM_USER")
            user_company.save()
        else:
            mailing, created = EmailTemplate.objects.get_or_create(
                company=company, email_type="REGISTER")

        confirmation_url = "%s/confirmation_user/%s" % (
            domain_pdf, user_company.hash_id
        )
        user = User.objects.get(email=user_company.email)
        # Send Email
        if mailing and mailing.from_email:
            context = dict()
            context["names"] = user_company.names
            context["first_name"] = user_company.names.split(" ")[0]
            context["email"] = user_company.email
            context["company"] = company
            context['confirmation_url'] = confirmation_url

            subject = mailing.subject
            e_mail = u'{0}<{1}>'.format(
                mailing.from_name, mailing.from_email)
            send_html_mail(
                subject, context, mailing.html_code, e_mail, [user_company.email, ],
                user_company, company, create_ticket, domain_pdf)

        return dict(success=True, message=message, confirm=status)


class GenerateUserCommunityPreferenceSerializer(serializers.Serializer):
    community_id = serializers.CharField()
    status = serializers.IntegerField()

    def create(self, validated_data):
        user = self.context.get("user")
        company = self.context.get("company")
        status = self.validated_data.get("status")
        community_id = self.validated_data.get("community_id")
        community = Community.objects.get(id=int(community_id))
        user_company = UserCompany.objects.get(
            company=company, user=user
        )
        if status:
            queryset = UserCommunityPreference.objects.filter(
                community=community, user_company=user_company,
                company=company
            )
            if not queryset:
                UserCommunityPreference.objects.create(
                    community=community, user_company=user_company,
                    company=company,
                )
        return dict(success=True)
