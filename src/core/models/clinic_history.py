from django.db import models

from core.models import User, TimeStampedUUIDModel
from django.utils.translation import gettext_lazy as _


class ClinicHistory(TimeStampedUUIDModel):
    """
    Clinic history for one user
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clinic_history',
        verbose_name=_('User'),
        help_text=_('User associated to the clinic history')
    )
    scholarship = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_('Scholarship'),
        help_text=_(
            'Field indicating whether the customer is suffering from scholarship.'
        )
    )
    hypertension = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_('Hypertension'),
        help_text=_(
            'Field that shows if the customer has an active hypertension.'
        )
    )
    diabetes = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_('Diabetes'),
        help_text=_(
            'Field indicating whether the customer is suffering from diabetes.'
        )
    )
    alcoholism = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_('Alcoholism'),
        help_text=_(
            'Field indicating whether the customer is suffering from alcoholism.'
        )
    )
    handicap = models.BooleanField(  # Migrate in the future to disabled
        blank=True,
        null=True,
        verbose_name=_('Handicap'),
        help_text=_(
            'Field indicating whether the customer is suffering from handicap.'
        )
    )
    active = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_('Active'),
        help_text=_(
            'Field indicating if the current clinic history is active. It should be only one active and it should be '
            'the last one'
        )
    )

    class Meta:
        verbose_name = _('Clinic history')
        verbose_name_plural = _('Clinic histories')

    def save(self, check_previous: bool = True, *args, **kwargs):
        """
        Check if there is another clinic history active for the user and deactivate it
        :param check_previous:
        :param args:
        :param kwargs:
        :return:
        """
        if check_previous and self.user.active_clinic_history:
            clinic_history_to_update = self.user.active_clinic_history
            clinic_history_to_update.active = False
            clinic_history_to_update.save(check_previous=False)
        super(ClinicHistory, self).save(*args, **kwargs)

    def same_clinic_history(self, clinic_history: 'ClinicHistory'):
        """
        Check if the clinic history is like other
        :param clinic_history:
        :return:
        """
        return (
            self.scholarship == clinic_history.scholarship and
            self.hypertension == clinic_history.hypertension and
            self.diabetes == clinic_history.diabetes and
            self.alcoholism == clinic_history.alcoholism and
            self.handicap == clinic_history.handicap
        )
