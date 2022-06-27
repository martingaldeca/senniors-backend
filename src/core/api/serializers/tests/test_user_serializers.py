from unittest import mock

from core.api.serializers import MeSerializer
from core.api.serializers import RegisterSerializer
from core.api.serializers import SimpleUserSerializer
from core.api.tests import SerializerTestBase
from core.exceptions import api as api_exceptions
from core.factories import UserFactory
from core.models import User


class SimpleUserSerializerTest(SerializerTestBase):

    def test_data(self):
        user: User = UserFactory()
        expected_data = {
            'uuid': user.uuid.hex,
            'username': user.username,
        }
        self.assertEqual(SimpleUserSerializer(instance=user, context=self.context).data, expected_data)


class MeSerializerTest(SerializerTestBase):
    def test_data(self):
        user: User = UserFactory()
        expected_data = {
            'uuid': user.uuid.hex,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'customer_type': user.customer_type,
            'birthdate': str(user.birthdate),
            'current_neighbourhood': user.current_neighbourhood,
        }
        self.assertEqual(MeSerializer(instance=user, context=self.context).data, expected_data)


class RegisterSerializerTest(SerializerTestBase):

    def test_validate_email_conflict(self):
        email = UserFactory().email
        data = {
            'username': 'test_username',
            'email': email,
            'password': 'testpass'
        }
        with self.assertRaises(api_exceptions.ConflictException) as expected_exception:
            RegisterSerializer(data=data, context=self.context).is_valid(raise_exception=True)
        self.assertEqual(expected_exception.exception.detail['message'], 'email-not-valid')

    def test_data(self):
        data = {
            'username': 'test_username',
            'email': 'test@test.com',
            'password': 'testpass'
        }
        serializer = RegisterSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        self.assertIsNone(serializer.data)

    def test_create(self):
        with mock.patch.object(User.objects, 'create_user') as mock_create_user:
            data = {
                'username': 'test_username',
                'email': 'test@test.com',
                'password': 'testpass'
            }
            serializer = RegisterSerializer(data=data, context=self.context)
            self.assertTrue(serializer.is_valid(raise_exception=True))
            serializer.create(serializer.validated_data)
            self.assertEqual(mock_create_user.call_count, 1)
            self.assertEqual(mock_create_user.call_args, mock.call(**data))
