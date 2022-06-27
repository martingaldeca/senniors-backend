from rest_framework import serializers

from core.api.serializers import ClinicHistorySerializer
from core.exceptions import api as api_exceptions
from core.models import ClinicHistory, User


class SimpleUserSerializer(serializers.ModelSerializer):
    """
    Simple user serializer with only the basic data
    """
    uuid = serializers.UUIDField(format='hex', read_only=True)

    class Meta:
        model = User
        fields = ['uuid', 'username']


class MeSerializer(SimpleUserSerializer):
    """
    Serializer for the clients to see the data associated to them
    """
    class Meta:
        model = User
        fields = [
            'uuid', 'username', 'email', 'first_name', 'last_name',
            'gender', 'customer_type', 'birthdate', 'current_neighbourhood',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register serializer to create new users
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    @staticmethod
    def validate_email(value):
        """
        Check if the email is not used by other user
        :param value:
        :return:
        """
        if User.objects.filter(email=value).exists():
            raise api_exceptions.ConflictException('email-not-valid')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    @property
    def data(self):
        return None


class CompleteUserSerializer(MeSerializer):
    """
    Serializer only allowed for admins to check all the user info including the active clinic history
    """

    active_clinic_history = ClinicHistorySerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'uuid', 'username', 'email', 'first_name', 'last_name',
            'gender', 'customer_type', 'age', 'birthdate', 'current_neighbourhood',
            'active_clinic_history'
        ]


class UpdateUserSerializer(CompleteUserSerializer):
    """
    Serializer used to update user info
    """
    scholarship = serializers.BooleanField(write_only=True, required=False)
    hypertension = serializers.BooleanField(write_only=True, required=False)
    diabetes = serializers.BooleanField(write_only=True, required=False)
    alcoholism = serializers.BooleanField(write_only=True, required=False)
    handicap = serializers.BooleanField(write_only=True, required=False)

    user_active_clinic_history: ClinicHistory = None

    class Meta:
        model = User
        fields = [
            'uuid', 'username', 'email', 'first_name', 'last_name',
            'gender', 'customer_type', 'age', 'birthdate', 'current_neighbourhood',
            'active_clinic_history',

            'scholarship', 'hypertension', 'diabetes', 'alcoholism', 'handicap',
        ]
        read_only_fields = ['uuid', 'username', 'age', 'active_clinic_history']

    def update(self, instance: User, validated_data):
        """
        If the user has not an active clinic history, one must be created, other case must check if any value changes
        :param instance:
        :param validated_data:
        :return:
        """
        self.user_active_clinic_history = instance.active_clinic_history

        if not self.user_active_clinic_history:
            ClinicHistory.objects.create(
                user=instance,
                scholarship=validated_data.get('scholarship'),
                hypertension=validated_data.get('hypertension'),
                diabetes=validated_data.get('diabetes'),
                alcoholism=validated_data.get('alcoholism'),
                handicap=validated_data.get('handicap'),
                active=True,
            )
        else:
            not_created_clinic_history = ClinicHistory(
                user=instance,
                scholarship=validated_data.get('scholarship'),
                hypertension=validated_data.get('hypertension'),
                diabetes=validated_data.get('diabetes'),
                alcoholism=validated_data.get('alcoholism'),
                handicap=validated_data.get('handicap'),
                active=True,
            )
            if not self.user_active_clinic_history.same_clinic_history(clinic_history=not_created_clinic_history):
                not_created_clinic_history.save()

        validated_data.pop('scholarship', None)
        validated_data.pop('hypertension', None)
        validated_data.pop('diabetes', None)
        validated_data.pop('alcoholism', None)
        validated_data.pop('handicap', None)
        return super(UpdateUserSerializer, self).update(instance, validated_data)
