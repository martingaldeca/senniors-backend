import uuid
from unittest import mock

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from core.api.serializers import CreateAppointmentSerializer
from core.api.tests import APITestBase
from core.models import Appointment


class CreateAppointmentViewTest(APITestBase):
    url = reverse('core:new_appointment')

    def test_post_201_CREATED(self):
        day = timezone.now().date()
        attendance_prediction = True
        data_to_send = {
            'user_uuid': self.user.uuid.hex,
            'day': str(day),
        }
        self.assertEqual(Appointment.objects.count(), 0)
        with mock.patch.object(
            Appointment,
            'attendance_prediction',
            new_callable=mock.PropertyMock
        ) as mock_attendance_prediction:
            mock_attendance_prediction.return_value = attendance_prediction
            response = self.client.post(self.url, data=data_to_send)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Appointment.objects.count(), 1)
            appointment = Appointment.objects.last()
            self.assertEqual(
                response.data,
                CreateAppointmentSerializer(instance=appointment).data
            )
