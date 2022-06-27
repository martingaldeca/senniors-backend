from django.utils import timezone
from factory import SubFactory
from factory.django import DjangoModelFactory

from core.factories import UserWithClinicHistoryFactory
from core.models import Appointment


class AppointmentFactory(DjangoModelFactory):
    class Meta:
        model = Appointment

    user = SubFactory(UserWithClinicHistoryFactory)
    scheduled = timezone.now()
    day = timezone.now().date()
    sms_received = timezone.now()
    attended = None
