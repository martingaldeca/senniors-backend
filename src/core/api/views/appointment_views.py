from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from core.api.serializers import CreateAppointmentSerializer


class CreateAppointmentView(CreateAPIView):
    """
    Main view to create a new appointment
    """
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CreateAppointmentSerializer
