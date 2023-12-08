from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


USERS_CREATE_URL = reverse('users:create')
TOKEN_CREATE_URL = reverse('users:token')

DEFAULT_USER_DATA = {
    'email': 'test@mail.com',
    'password': 'pass123!"# ',
    'first_name': 'Test',
    'last_name': 'User'
}


def create_user():
    return get_user_model().objects.create_user(**DEFAULT_USER_DATA)


class PubliUserApiTets(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):

        res = self.client.post(USERS_CREATE_URL, DEFAULT_USER_DATA)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=DEFAULT_USER_DATA['email'])
        self.assertTrue(user.check_password(DEFAULT_USER_DATA['password']))
        self.assertNotIn('password', res.json())

    def test_create_token(self):

        create_user()

        payload = {
            'email': DEFAULT_USER_DATA['email'],
            'password': DEFAULT_USER_DATA['password']
        }

        res = self.client.post(TOKEN_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.json())