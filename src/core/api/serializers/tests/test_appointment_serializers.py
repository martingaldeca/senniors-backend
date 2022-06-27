import uuid
from unittest import mock

from django.utils import timezone

from core.api.serializers import CompleteUserSerializer, MeSerializer
from core.api.serializers import CreateAppointmentSerializer
from core.api.serializers import SimpleUserSerializer
from core.api.tests import SerializerTestBase
from core.exceptions import api as api_exceptions
from core.factories import UserWithClinicHistoryFactory
from core.factories.appointment_factories import AppointmentFactory
from core.models import Appointment, User


class CreateAppointmentSerializerTest(SerializerTestBase):

    def setUp(self) -> None:
        self.user = UserWithClinicHistoryFactory()
        self.day = timezone.now().date()
        self.data = {
            'user_uuid': self.user.uuid.hex,
            'day': str(self.day),
        }
        self.attendance_prediction = True
        self.instance: Appointment = AppointmentFactory(user=self.user)
        self.expected_data = {
            'uuid': self.instance.uuid.hex,
            'user': CompleteUserSerializer(instance=self.instance.user).data,
            'scheduled': self.instance.scheduled.astimezone().isoformat(),
            'day': str(self.instance.day),
            'sms_received': self.instance.sms_received.astimezone().isoformat(),
            'attendance_prediction': self.attendance_prediction,
            'days_until_appointment': 0
        }

    def test_validate_user_uuid_not_found(self):
        data = self.data.copy()
        data['user_uuid'] = uuid.uuid4().hex

        with self.assertRaises(
            api_exceptions.NotFoundException
        ) as expected_exception:
            CreateAppointmentSerializer(data=data).is_valid(raise_exception=True)
        self.assertEqual(expected_exception.exception.detail['message'], 'user-not-found')

    def test_validate_day_not_in_future(self):
        data = self.data.copy()
        data['day'] = '1994-08-08'

        with self.assertRaises(
            api_exceptions.BadRequestException
        ) as expected_exception:
            CreateAppointmentSerializer(data=data).is_valid(raise_exception=True)
        self.assertEqual(expected_exception.exception.detail['message'], 'day-must-be-in-future')

    def test_data(self):
        serializer = CreateAppointmentSerializer(instance=self.instance)
        with mock.patch.object(
            Appointment,
            'attendance_prediction',
            new_callable=mock.PropertyMock
        ) as mock_attendance_prediction:
            mock_attendance_prediction.return_value = self.attendance_prediction
            self.assertEqual(
                serializer.data,
                self.expected_data
            )

    def test_create(self):
        with mock.patch.object(
            Appointment.objects, 'create'
        ) as mock_create_appointment:

            serializer = CreateAppointmentSerializer(data=self.data)
            self.assertTrue(serializer.is_valid(raise_exception=True))
            serializer.create(serializer.validated_data)
            self.assertEqual(mock_create_appointment.call_count, 1)
            self.assertEqual(
                mock_create_appointment.call_args,
                mock.call(
                    day=self.day,
                    user=self.user
                )
            )
