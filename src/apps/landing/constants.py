from django import forms
from src.apps.companies.models import JobCompany, Occupation
from src.apps.conf.models import Country


forms_dict = {
    'names': forms.CharField(),
    'last_name': forms.CharField(),
    'phone': forms.CharField(),
    'occupation': forms.CharField(required=False),
    'job_company': forms.CharField(required=False),
    'company_position': forms.CharField(required=False),
    'occupation_select': forms.ModelChoiceField(
        queryset=Occupation.objects.order_by('position'),
        empty_label="Profesión",
        required=False),
    'job_company_select': forms.ModelChoiceField(
        queryset=JobCompany.objects.order_by('position'),
        empty_label="Empresa",
        required=False),
    'country': forms.ModelChoiceField(
        queryset=Country.objects.order_by('position'),
        empty_label="País",
        required=False),
    }
