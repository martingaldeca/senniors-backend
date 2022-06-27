from django.utils import timezone

from core.api.serializers import CompleteUserSerializer
from core.exceptions.api import BadRequestException, NotFoundException
from core.models import Appointment, User
from rest_framework import serializers


class CreateAppointmentSerializer(serializers.ModelSerializer):
    """
    This serializer is in charge of create the appointment in the database.
    It will return all the appointment info, including the attendance data prediction.
    """
    uuid = serializers.UUIDField(read_only=True, format='hex')
    user = CompleteUserSerializer(read_only=True)

    user_uuid = serializers.UUIDField(write_only=True, format='hex')

    class Meta:
        model = Appointment
        fields = [
            'uuid', 'user_uuid', 'user', 'scheduled', 'day', 'sms_received', 'attendance_prediction',
            'days_until_appointment'
        ]
        read_only_fields = ['sms_received', 'attendance_prediction', 'scheduled', 'days_until_appointment']
        extra_kwargs = {
            'day': {'required': True},
        }

    def create(self, validated_data):
        """
        Appointment receives when created not user_uuid, so we will update the name of the key
        :param validated_data:
        :return:
        """
        validated_data['user'] = validated_data.pop('user_uuid')
        return super(CreateAppointmentSerializer, self).create(validated_data)

    @staticmethod
    def validate_user_uuid(value):
        """
        Must validate that the user uuid exist, if not a 404 will be raised
        :param value:
        :return:
        """
        qs = User.objects.filter(uuid=value)
        if qs.exists():
            return qs.last()
        raise NotFoundException('user-not-found')

    @staticmethod
    def validate_day(value):
        """
        Must validate that the day is not in the past, if it is a 400 will be raised
        :param value:
        :return:
        """
        if timezone.now().date() > value:
            raise BadRequestException('day-must-be-in-future')
        return value
