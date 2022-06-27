from unittest import mock

from core.api.serializers import MeSerializer
from core.api.serializers import RegisterSerializer
from core.api.serializers import ClinicHistorySerializer
from core.api.tests import SerializerTestBase
from core.exceptions import api as api_exceptions
from core.factories import ClinicHistoryFactory
from core.models import ClinicHistory


class ClinicHistorySerializerTest(SerializerTestBase):

    def test_data(self):
        clinic_history: ClinicHistory = ClinicHistoryFactory()
        expected_data = {
            'uuid': clinic_history.uuid.hex,
            'scholarship': clinic_history.scholarship,
            'hypertension': clinic_history.hypertension,
            'diabetes': clinic_history.diabetes,
            'alcoholism': clinic_history.alcoholism,
            'handicap': clinic_history.handicap,
            'active': clinic_history.active,
        }
        self.assertEqual(ClinicHistorySerializer(instance=clinic_history, context=self.context).data, expected_data)