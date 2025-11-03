from rest_framework import serializers
from src.apps.landing.models import CustomerInvitedLanding
from src.apps.companies.models import Company, UserCompany
import xlrd
from src.apps.customers.models import Customer
from src.apps.users.models import User
from src.apps.tickets.utils import generate_ticket_code
from src.apps.landing.utils import record_to_pdf


class CustomerInvitedListSerializer(serializers.Serializer):
    excel = serializers.FileField()
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(),
        slug_field='name',
        label="Selecciona una Companía"
    )

    def create(self, validated_data):
        company = validated_data.pop("company")
        file = validated_data.pop('excel')
        book = xlrd.open_workbook(file_contents=file.read())
        sh = book.sheet_by_index(0)
        for rx in range(1, sh.nrows):
            email = sh.cell_value(rowx=rx, colx=0).lower()
            first_name = sh.cell_value(rowx=rx, colx=1).title()
            first_surname = sh.cell_value(rowx=rx, colx=2).title()
            in_person = True
            try:
                in_person = int(sh.cell_value(rowx=rx, colx=3))
            except Exception as e:
                print(e)

            virtual = True
            try:
                virtual = int(sh.cell_value(rowx=rx, colx=4))
            except Exception as e:
                print(e)
            names = f"{first_name} {first_surname}"
            if not CustomerInvitedLanding.objects.filter(
                company=company, email=email
            ).all():
                CustomerInvitedLanding.objects.get_or_create(
                    email=email, first_name=first_name,
                    first_surname=first_surname, names=names,
                    in_person=in_person, virtual=virtual,
                    company=company
                )
            else:
                print(email, 'ALREADY IN LIST')
        return {"message": "SUCCESS"}


class GenerateCustomerExcelSerializer(serializers.Serializer):
    excel = serializers.FileField()
    create_tickets = serializers.BooleanField()
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(),
        slug_field='name',
        label="Selecciona una Companía"
    )

    def create(self, validated_data):
        company = validated_data.pop("company")
        file = validated_data.pop('excel')
        create_tickets = validated_data.pop('create_tickets')
        book = xlrd.open_workbook(file_contents=file.read())
        sh = book.sheet_by_index(0)
        new_customers = []
        for rx in range(1, sh.nrows):
            email = sh.cell_value(rowx=rx, colx=0)
            name = sh.cell_value(rowx=rx, colx=1)
            password = sh.cell_value(rowx=rx, colx=2)
            customers = Customer.objects.filter(email=email)
            if customers:
                customer = customers.last()
            else:
                customer = Customer.objects.create(
                    email=email, names=name,
                    password=password
                )
                customer.set_password(password)
                customer.save()
            if not UserCompany.objects.filter(email=email.lower(), company=company):
                user = User.objects.get(email=customer.email)
                user_company = UserCompany.objects.create(
                    email=email,
                    user=user,
                    full_name=name,
                    in_person=True,
                    virtual=True,
                    confirmed=True,
                    company=company
                )
                user_company.set_password(password)
                user_company.save()
                if create_tickets:
                    domain = f"https://{company.domain}"
                    generate_ticket_code(user_company.user, company)
                    record_to_pdf(user_company.user, domain, company)
        return {"new_customers": len(new_customers)}
