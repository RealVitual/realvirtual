from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Customer


class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('email', 'first_name')

    def __init__(self, *args, **kargs):
        super(CustomerCreationForm, self).__init__(*args, **kargs)


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kargs):
        super(CustomerChangeForm, self).__init__(*args, **kargs)
