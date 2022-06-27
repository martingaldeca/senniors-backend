from factory import SubFactory
from factory.django import DjangoModelFactory

from core.factories import UserFactory
from core.models import ClinicHistory


class ClinicHistoryFactory(DjangoModelFactory):
    class Meta:
        model = ClinicHistory

    user = SubFactory(UserFactory)
    scholarship = False
    hypertension = False
    diabetes = False
    alcoholism = False
    handicap = False
    active = True
