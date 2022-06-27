import factory
from django.utils import timezone
from factory.fuzzy import FuzzyText

from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_staff = False
    is_active = True
    is_superuser = False
    gender = User.G_FEMALE
    customer_type = User.T_PATIENT
    birthdate = timezone.now().date()
    current_neighbourhood = FuzzyText()


class UserWithClinicHistoryFactory(UserFactory):
    @factory.post_generation
    def clinic_history(self: User, create, extracted, **kwargs):
        from core.factories import ClinicHistoryFactory
        ClinicHistoryFactory(user=self)
