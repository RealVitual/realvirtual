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
from django.conf import settings
from django.core.mail import get_connection


def send_html_mail(subject, html_content, e_mail, receptors,
                   customer, company):
    EmailThread(
        subject, html_content, e_mail, receptors,
        customer, company).start()


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content,
                 e_mail, receptors, customer, company):
        self.subject = subject
        self.e_mail = e_mail
        self.html_content = html_content
        self.receptors = receptors
        self.customer = customer
        self.company = company
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
        if status:
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
        tickets = user.user_tickets.filter(company=company)
        url_ticket = ""
        if tickets:
            ticket = tickets.last()
            url_ticket = "%s/download_ticket/%s" % (
                domain_pdf, ticket.hash_id
            )
        # Send Email
        print(company, 'COMPANY')
        if mailing and mailing.from_email:
            context = dict()
            context["names"] = user_company.names
            context["first_name"] = user_company.names.split(" ")[0]
            context["email"] = user_company.email
            context["company"] = company
            context['url_ticket'] = url_ticket
            context['confirmation_url'] = confirmation_url

            template = Template(mailing.html_code)
            html_content = template.render(Context(context))
            subject = mailing.subject
            e_mail = u'{0}<{1}>'.format(
                mailing.from_name, mailing.from_email)
            # msg = EmailMessage(
            #     subject, html_content, e_mail, [user_company.email, ])
            # msg.content_subtype = "html"
            send_html_mail(
                subject, html_content, e_mail, [user_company.email, ],
                user_company, company)

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
