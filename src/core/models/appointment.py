from django.db import models
from django.utils import timezone

from core.helpers.data_client import DataClient
from core.models import TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _

from core.models import User


class Appointment(TimeStampedUUIDModel):
    """
    This model represents an appointment for one user and save the info in the database
    """

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_clinic_history',
        verbose_name=_('Clinic history'),
        help_text=_('Clinic history of the user.')
    )
    scheduled = models.DateTimeField(
        blank=True,
        null=True,
        auto_now_add=True,
        verbose_name=_('Scheduled'),
        help_text=_('Date when the appointment was scheduled.')
    )
    day = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Day'),
        help_text=_('Day when the appointment will take place.')
    )
    sms_received = models.DateTimeField(  # Backend for that is quite difficult (it is a full code test)
        blank=True,
        null=True,
        verbose_name=_('Sms received'),
        help_text=_('The moment when the user receives the sms.')
    )
    attended = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_('Attendance'),
        help_text=_('Field that show if the user attended the appointment.')
    )

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')

    @property
    def has_sms_received(self):
        """
        Transform to bool the datetime of sms_receive
        :return:
        """
        return bool(self.sms_received)

    @property
    def attendance_prediction(self) -> bool:
        """
        Use the data client to call brain services and predict if attending
        :return:
        """
        input_data = {
            'gender': self.user.int_gender,
            'scheduled_day': self.scheduled.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'appointment_day': self.day.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'age': self.user.age,
            'neighbourhood': self.user.current_neighbourhood,
            'scholarship': int(self.user.active_clinic_history.scholarship) if self.user.active_clinic_history else 0,
            'hypertension': int(self.user.active_clinic_history.scholarship) if self.user.active_clinic_history else 0,
            'diabetes': int(self.user.active_clinic_history.scholarship) if self.user.active_clinic_history else 0,
            'alcoholism': int(self.user.active_clinic_history.scholarship) if self.user.active_clinic_history else 0,
            'handicap': int(self.user.active_clinic_history.handicap) if self.user.active_clinic_history else 0,
            'sms_received': int(bool(self.sms_received)),
        }
        return DataClient().predict_attending(input_data=input_data)

    @property
    def days_until_appointment(self) -> int:
        """
        Return the days until the appointment from now
        :return:
        """
        return (self.day - timezone.now().date()).days
