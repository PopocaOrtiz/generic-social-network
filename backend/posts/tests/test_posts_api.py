from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


POSTS_URL = reverse('posts:post-list')


class PublicPostsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_posts(self):

        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 0)