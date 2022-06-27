from django.urls import reverse
from rest_framework import status

from core.api.serializers import CompleteUserSerializer, MeSerializer, UpdateUserSerializer
from core.api.tests import APITestBase
from core.models import User


class RegisterViewTest(APITestBase):
    url = reverse('core:register')

    def test_post_201_CREATED(self):
        username = 'test'
        email = 'test@test.test'
        password = 'testpass'
        data_to_send = {
            'username': username,
            'email': email,
            'password': password,
        }
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(self.url, data=data_to_send)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.last()
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


class MeDetailViewTest(APITestBase):
    url = reverse('core:me')

    def test_get_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MeSerializer(instance=self.user).data)


class ListUsersViewTest(APITestBase):
    url = reverse('core:users')

    def test_get_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'],
            [CompleteUserSerializer(instance=self.user).data, ]
        )


class UpdateUserViewTest(APITestBase):
    url = reverse('core:update_user', kwargs={'user_uuid': None})

    def test_update_user_200_OK(self):
        self.url = reverse('core:update_user', kwargs={'user_uuid': self.user.uuid.hex})
        new_first_name = 'Test name'
        data = {
            'first_name': new_first_name
        }
        response = self.client.put(self.url, data=data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            UpdateUserSerializer(instance=self.user).data
        )
        self.assertEqual(self.user.first_name, new_first_name)
