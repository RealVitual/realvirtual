from rest_framework.views import APIView
from .serializers import (
    CustomerInvitedListSerializer,
    GenerateCustomerExcelSerializer)
from src.apps.users.permissions import AdminAuthenticatedPermission
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse


class GenerateInvitedEmail(APIView):
    serializer_class = CustomerInvitedListSerializer
    permission_classes = [AdminAuthenticatedPermission]

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return redirect(reverse(
                'customers:generate_landing_invited'))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateCustomers(APIView):
    serializer_class = GenerateCustomerExcelSerializer
    permission_classes = [AdminAuthenticatedPermission]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            res = serializer.save()
            return HttpResponse(res, status=status.HTTP_200_OK)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
