from rest_framework import serializers
from src.apps.landing.models import CustomerInvitedLanding
import xlrd


class CustomerInvitedListSerializer(serializers.Serializer):
    excel = serializers.FileField()

    def create(self, validated_data):
        company = self.context.get("company")
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
