from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core import mail
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

from posts.models import Post, Comment
from posts.serializers import CommentSerializer


User = get_user_model()


def build_posts_comments_url(post_id):
    return reverse('posts:comments', args=[post_id])


def build_comment_detail_url(comment_id):
    return reverse('posts:comment-detail', args=[comment_id])


class CommentModelTest(TestCase):

    def test_comment_must_be_assigned(self):

        user = baker.make(User)

        with self.assertRaises(ValidationError):
            Comment.objects.create(
                content='comment content',
                author=user
            )


class PublicCommentsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_comments(self):

        post = baker.make(Post)  # type: Post
        baker.make(Comment, post=post)
        baker.make(Comment, post=post)

        another_post = baker.make(Post)  # type: Post
        baker.make(Comment, post=another_post)

        url = build_posts_comments_url(post.id)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        serializer = CommentSerializer(Comment.objects.filter(post=post), many=True)
        self.assertEquals(res.data, serializer.data)

    def test_get_comment(self):
        """test a comment can be assigned to another comment"""
        post = baker.make(Post)
        post_comment = baker.make(Comment, post=post)
        post_comment_comment1 = baker.make(Comment, comment=post_comment)
        post_comment_comment2 = baker.make(Comment, comment=post_comment)
        post_comment_comment1_comment = baker.make(Comment, comment=post_comment_comment1)

        serializer = CommentSerializer(post_comment)

        url = build_comment_detail_url(post_comment.id)
        
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_comment_fail(self):
        
        post = baker.make(Post)

        payload = {
            'content': 'comment content',
            'post': post.id,
        }

        url = build_posts_comments_url(post.id)

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        

class PrivateCommentsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@mail.com')
        self.client.force_authenticate(self.user)

    def test_create_comment(self):

        post = baker.make(Post, author=baker.make(get_user_model()))

        payload = {
            'post': post.id,
            'content': 'comment content'
        }

        url = build_posts_comments_url(post.id)

        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.json()['content'], payload['content'])

        self.assertEqual(len(mail.outbox), 1)

        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.to, [post.author.email])