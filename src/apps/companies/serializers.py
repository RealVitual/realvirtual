from rest_framework import serializers
from .models import UserCompany


class CustomerListSerializer(serializers.ModelSerializer):
    company_position = serializers.SerializerMethodField()
    job_company = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    company_position = serializers.SerializerMethodField()
    occupation = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserCompany
        fields = ('full_name', 'email',
                  'occupation', 'company_position', 'country', 'job_company')

    def get_occupation(self, obj):
        return obj.user.occupation

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_country(self, obj):
        if obj.user.country:
            return obj.user.country.name
        return ""

    def get_company_position(self, obj):
        return obj.user.company_position

    def get_job_company(self, obj):
        return obj.user.job_company


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = ('first_name', 'first_surname',
                  'last_surname', 'email', 'gender', 'document_type',
                  'document', 'date_birth', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = UserCompany(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer
