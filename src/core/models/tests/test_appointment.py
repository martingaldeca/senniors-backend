from unittest import mock

from django.test import TestCase
from django.utils import timezone

from core.factories.appointment_factories import AppointmentFactory
from core.helpers.data_client import DataClient
from core.models import Appointment


class AppointmentTest(TestCase):

    def setUp(self) -> None:
        self.appointment: Appointment = AppointmentFactory()

    def test_has_sms_received(self):
        test_data_list = [
            (timezone.now(), True),
            (None, False),
        ]

        for test_data in test_data_list:
            with self.subTest(
                test_data=test_data
            ), mock.patch.object(
                Appointment, 'sms_received', new_callable=mock.PropertyMock
            ) as mock_sms_received:
                sms_received, expected = test_data
                mock_sms_received.return_value = sms_received
                self.assertEqual(self.appointment.has_sms_received, expected)

    def test_attendance_prediction(self):
        with mock.patch.object(
            DataClient, 'predict_attending'
        ) as mock_predict_attending:
            mock_predict_attending.return_value = True
            expected_input_data = {
                'gender': self.appointment.user.int_gender,
                'scheduled_day': self.appointment.scheduled.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'appointment_day': self.appointment.day.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'age': self.appointment.user.age,
                'neighbourhood': self.appointment.user.current_neighbourhood,
                'scholarship': int(self.appointment.user.active_clinic_history.scholarship),
                'hypertension': int(self.appointment.user.active_clinic_history.scholarship),
                'diabetes': int(self.appointment.user.active_clinic_history.scholarship),
                'alcoholism': int(self.appointment.user.active_clinic_history.scholarship),
                'handicap': int(self.appointment.user.active_clinic_history.handicap),
                'sms_received': int(bool(self.appointment.sms_received)),
            }
            self.assertTrue(self.appointment.attendance_prediction)
            self.assertEqual(mock_predict_attending.call_count, 1)
            self.assertEqual(
                mock_predict_attending.call_args,
                mock.call(
                    input_data=expected_input_data
                )
            )
