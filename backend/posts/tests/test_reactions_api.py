from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker


from posts import models, serializers


def build_reactions_url(post_id):
    return reverse('posts:reaction-list', args=[post_id])


def build_reaction_detail_url(post_id, reaction_id):
    return reverse('posts:reaction-detail', args=[post_id, reaction_id])


def build_comment_reactions_url(post_id, comment_id):
    return reverse('posts:comment-reactions', args=[post_id, comment_id])


class PublicReactionsAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_post_reactions(self):

        user = get_user_model().objects.create(email='test@mail.com')

        post = baker.make(models.Post)
        models.Reaction.objects.create(
            user=user,
            post=post
        )

        another_post = baker.make(models.Post)
        models.Reaction.objects.create(
            user=user,
            post=another_post
        )

        url = build_reactions_url(post.id)
        res = self.client.get(url)

        self.assertEquals(res.status_code, status.HTTP_200_OK)

        serializer = serializers.ReactionSerializer(models.Reaction.objects.filter(post=post), many=True)
        self.assertEqual(res.data, serializer.data)

    def test_get_comment_reactions(self):

        user = get_user_model().objects.create(email='test@mail.com')

        post = baker.make(models.Post)

        models.Reaction.objects.create(
            user=user,
            post=post
        )

        comment = models.Comment.objects.create(
            author=user,
            content='test comment',
            post=post
        )

        models.Reaction.objects.create(user=user, comment=comment)

        url = build_comment_reactions_url(post.id, comment.id)
        res = self.client.get(url)

        self.assertEquals(res.status_code, status.HTTP_200_OK)

        reactions = models.Reaction.objects.filter(comment=comment)
        serializer = serializers.ReactionSerializer(reactions, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.json()), reactions.count())

    def test_send_reaction_fail(self):

        post = baker.make(models.Post)

        payload = {
            'type': 'like',
        }

        url = build_reactions_url(post.id)
        
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateReactionsAPITests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(email='test@mail.com')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_send_reaction(self):

        post = baker.make(models.Post)

        queryset = models.Reaction.objects.filter(post=post)

        url = build_reactions_url(post.id)

        payload = {
            'type': models.Reaction.TYPES[0][0]
        }

        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(queryset.count(), 1)

        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(queryset.count(), 1)

        res = self.client.delete(build_reaction_detail_url(post.id, res.json()['id']), payload)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(queryset.count(), 0)
