from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


USERS_URL = reverse('users:user-list')


class PubliUserApiTets(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_emtpy_users(self):

        res = self.client.get(USERS_URL)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.json()), 0)