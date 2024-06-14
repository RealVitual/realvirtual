import abc
from .models import CustomerInvitedLanding
from src.apps.companies.constants import AccessType


class AccessCustomerContext(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        self.data = kwargs.get('data')
        self.domain = kwargs.get('domain')
        self.company = kwargs.get('company')
        self.customer = None
        self.password = None
        self.message = ""
        self.validated_user = True
        self.response = {}
        # self.reg_rules, created = RegistrationRules.objects.get_or_create(
        #     pk=1
        # )

    @abc.abstractmethod
    def validate_access(self):
        message = ""
        access_type = self.company.access_type
        if self.company.is_private:
            found_invited_customer = CustomerInvitedLanding.objects.filter(
                company=self.company, email=self.date.get('email'))
            if found_invited_customer:
                return True
            elif self.company.allow_virtual_access and \
                    access_type == AccessType.HYBRID.value:
                message = "Sólo Podrás acceder al evento de forma virtual. ¿Deseas continuar?"  # noqa
                return True
            else:
                message = "No estás en la base de datos de invitados"
                return False
        if access_type in [
                AccessType.HYBRID.value, AccessType.IN_PERSON.value]:
            if self.company.current_quantity > self.company.capacity:
                return True
            elif access_type == AccessType.IN_PERSON.value:
                message = "Lo sentimos, el aforo está completo"
                return False
            else:
                message = "Sólo Podrás acceder al evento de forma virtual. ¿Deseas continuar?"
                return True

    @abc.abstractmethod
    def create_user(self):
        pass

    @abc.abstractmethod
    def set_route(self):
        pass

    @abc.abstractmethod
    def build_message(self):
        pass

    def build_credential(self):
        # if self.reg_rules.generate_credential:
        #     generate_credential(self.customer)
        pass

    @abc.abstractmethod
    def build_response(self):
        pass


class PublicAccessStrategy(AccessCustomerContext):
    def create_user(self):
        if self.validate_access():
            self.data['company_id'] = self.company.id
            self.data['in_person'] = self.company.in_person
            "Customer.objects.create(**self.data)"
        return False

    def set_route(self):
        pass
