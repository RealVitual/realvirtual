from rest_framework.views import APIView
from .serializers import CustomerInvitedListSerializer
from src.apps.users.permissions import AuthenticatedPermission
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse


class GenerateInvitedEmail(APIView):
    serializer_class = CustomerInvitedListSerializer
    permission_classes = [AuthenticatedPermission]

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'company': request.company
                }
            )
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse(
                'customers:generate_landing_invited'))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
