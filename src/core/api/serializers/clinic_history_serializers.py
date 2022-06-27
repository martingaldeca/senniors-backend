from core.models import ClinicHistory
from rest_framework import serializers


class ClinicHistorySerializer(serializers.ModelSerializer):
    """
    This serializer returns a clinic history without the user information
    """
    uuid = serializers.UUIDField(format='hex')

    class Meta:
        model = ClinicHistory
        fields = [
            'uuid', 'scholarship', 'hypertension', 'diabetes', 'alcoholism', 'handicap', 'active'
        ]
