from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker


from posts import serializers, models


POSTS_URL = reverse('posts:post-list')


class PublicPostsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_empty_posts(self):

        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 0)

    def test_get_posts(self):

        baker.make(models.Post)
        baker.make(models.Post)

        res = self.client.get(POSTS_URL)

        posts = models.Post.objects.all()
        serializer = serializers.PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_fail_create(self):

        payload = {
            'content': 'post content'
        }

        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePostAPITests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(email='test@mail.com')

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_post(self):

        payload = {
            'content': 'post content'
        }

        res = self.client.post(POSTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        serializer = serializers.PostSerializer(models.Post.objects.get(id=res.json()['id']))
        self.assertEqual(res.data, serializer.data)