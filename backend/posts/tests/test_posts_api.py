import os
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APIRequestFactory
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
        request = APIRequestFactory().get(POSTS_URL)
        serializer = serializers.PostSerializer(posts, many=True, context={'request': request})

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

        request = APIRequestFactory().get(POSTS_URL)
        serializer = serializers.PostSerializer(models.Post.objects.get(id=res.json()['id']), context={'request': request})
        self.assertEqual(res.data, serializer.data)

    @patch('aws.facades.s3.S3.upload_in_memory_file')
    def test_create_post_with_image(self, mock_upload_in_memory_field):

        mock_url = 'https://bucket.aws.com/image.png'
        mock_upload_in_memory_field.return_value = mock_url

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/dummy-image.png')

        with open(file_path, 'rb') as file:
            payload = {
                'content': 'post content',
                'image_file': SimpleUploadedFile('test.png', file.read(), content_type='image/png'),
            }

            res = self.client.post(POSTS_URL, payload, format='multipart')

            self.assertEquals(res.status_code, status.HTTP_201_CREATED)
            self.assertIn('image', res.data)
            self.assertEqual(res.data['image'], mock_url)

            mock_upload_in_memory_field.assert_called_once()