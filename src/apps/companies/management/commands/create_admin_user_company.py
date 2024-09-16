from django.core.management.base import BaseCommand
from src.apps.users.models import User
from src.apps.companies.models import Company, UserCompany


class Command(BaseCommand):
    help = 'Create a user for company'

    def handle(self, *args, **kwargs):
        companies = Company.objects.order_by('name').values_list(
            'name', flat=True)
        email = input('Ingrese email: ')
        self.stdout.write(self.style.SUCCESS('Compañías disponibles:'))
        for company in companies:
            self.stdout.write(f"- {company}")
        while True:
            company_name = input('Ingrese nombre de una de las compañía existentes: ') # noqa
            if not company_name or company_name not in companies:
                self.stdout.write(self.style.ERROR(
                    'Ingrese el nombre de una compañía válida. Inténtelo de nuevo.')) # noqa
            else:
                break
        password = input('Ingrese contraseña: ')
        while True:
            confirm_password = input('Ingrese nuevamente la contraseña: ')
            if not password == confirm_password:
                self.stdout.write(self.style.ERROR('Las contraseñas no coinciden')) # noqa
            else:
                break

        user, created = User.objects.get_or_create(email=email)
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Usuario {email} creado exitosamente'))
            user.password = password
            user.set_password(password)
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Usuario {email} ya existe'))

        company = Company.objects.get(name=company_name)

        user_company, user_company_created = UserCompany.objects.get_or_create(
            company=company, user=user, email=email)
        if user_company_created:
            self.stdout.write(self.style.SUCCESS(
                f'Usuario con {email} creado para company {company_name}'))
            user_company.is_admin = True
            user_company.set_password(password)
            user_company.save()
        else:
            self.stdout.write(self.style.WARNING(
                f'Usuario con {email} creado para company {company_name} y existe')) # noqa
            raise ValueError('User Company ya existe')
