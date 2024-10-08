from .serializers import GenerateCustomerScheduleSerializer
from  src.apps.users.permissions import AuthenticatedPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GenerateScheduleCustomerEvent(APIView):
    serializer_class = GenerateCustomerScheduleSerializer
    permission_classes = [AuthenticatedPermission]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'user': request.user,
                'company': request.company})
        if serializer.is_valid():
            serializer.save()
            return Response(dict(
                success=True), status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
