from rest_framework import serializers
from src.apps.users.models import User
from src.apps.events.models import Schedule, ScheduleCustomerEvent


class GenerateCustomerScheduleSerializer(serializers.Serializer):
    schedule_id = serializers.CharField()
    status = serializers.IntegerField()

    def create(self, validated_data):
        print(self.context, 'CONTEXT')
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
        else:
            ScheduleCustomerEvent.objects.filter(
                schedule_id=schedule_id, user=user,
                event_id=schedule.event.id,
                company=company
            ).delete()
            # rules_email, created = EmailRules.objects.get_or_create(pk=1)
            # # Send Email
            # if rules_email.schedule_mail:
            #     context = dict()
            #     context["names"] = user.names
            #     context["first_name"] = user.names.split(" ")[0]
            #     context["email"] = user.email
            #     context["event"] = event
            #     email_type = "SCHEDULE"
            #     mail = AutomaticSingleMail(
            #         context=context, receptor=user,
            #         email_type=email_type)
            #     mail.send_mail()
            # End SendEmail
        return dict(success=True)
