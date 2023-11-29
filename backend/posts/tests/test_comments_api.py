from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from model_bakery import baker

from posts.models import Post, Comment
from posts.serializers import CommentSerializer
from users.models import User


def build_comments_url(post_id):
    return reverse('posts:comments', args=[post_id])


class PublicCommentsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_comments(self):

        post = baker.make(Post)  # type: Post
        post.comments.add(baker.make(Comment))
        post.comments.add(baker.make(Comment))

        another_post = baker.make(Post)  # type: Post
        post.comments.add(baker.make(Comment))

        url = build_comments_url(post.id)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        serializer = CommentSerializer(Comment.objects.filter(post=post), many=True)
        self.assertEquals(res.data, serializer.data)

    def test_create_comment_fail(self):
        
        post = baker.make(Post)

        payload = {
            'content': 'comment content',
            'post': post.id,
        }

        url = build_comments_url(post.id)

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        

class PrivateCommentsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.com')
        self.client.force_authenticate(self.user)

    def test_create_comment(self):

        post = baker.make(Post)

        payload = {
            'post': post.id,
            'content': 'comment content'
        }

        url = build_comments_url(post.id)

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.json()['content'], payload['content'])