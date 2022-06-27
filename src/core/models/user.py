from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedUUIDModel
from django.db import models


class User(AbstractUser, TimeStampedUUIDModel):
    """
    It represents a customer
    """
    G_MALE, G_FEMALE = 'm', 'f'
    ALLOWED_GENDERS = (
        (G_MALE, _('Male')),
        (G_FEMALE, _('Female')),
    )

    T_PATIENT, T_FAMILIAR = 'patient', 'familiar'
    ALLOWED_TYPES = (
        (T_PATIENT, _('Patient')),
        (T_FAMILIAR, _('Familiar')),
    )

    gender = models.CharField(
        max_length=4,
        choices=ALLOWED_GENDERS,
        blank=True,
        null=True,
        verbose_name=_('Gender'),
        help_text=_('Gender of the customer, it can be (for now), male (m) or female (f).')
    )
    customer_type = models.CharField(
        max_length=10,
        choices=ALLOWED_TYPES,
        blank=True,
        null=True,
        verbose_name=_('Customer type'),
        help_text=_('Type of the customer, it can be a patient or a familiar.')
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Birthday'),
        help_text=_('Birthday of teh customer.')
    )
    current_neighbourhood = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_('Current neighbourhood'),
        help_text=_(
            'Current neighbourhood of the customer, it can change if in the future the customer moves to another.'
        )
    )

    @property
    def age(self):
        """
        Property that shows the age of the customer when it is called
        :return: int
        """
        return timezone.now().year - self.birthdate.year

    @property
    def active_clinic_history(self) -> 'ClinicHistory':
        """
        Return the last active clinic history for the user (it should be only one), if there is not an active clinic
        history it will return None
        :return:
        """
        qs = self.clinic_history.filter(active=True)
        if qs.exists():
            return qs.last()

    @property
    def int_gender(self):
        """
        Transform the gender to int in order to pass it to the brain-services
        :return:
        """
        if self.gender == self.G_MALE:
            return 0
        if self.gender == self.G_FEMALE:
            return 1
        return -1
