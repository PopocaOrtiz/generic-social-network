import pytest
from rest_framework import status
from django.urls import reverse

from posts import models


@pytest.fixture
def save_post():
    def create_save(post, user):
        save = models.Save.objects.create(post=post, user=user)
        return save
    return create_save


@pytest.mark.django_db
@pytest.mark.xfail
def test_save_post(auth_client, create_post):
    client, user = auth_client()
    post = create_post()
    url = reverse('posts:post-save', args=[post.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.xfail
def test_fetch_saved_posts(auth_client, create_post, save_post):

    client, user = auth_client()

    post1 = create_post()
    post2 = create_post()
    post3 = create_post()

    save_post(post1, user)
    save_post(post2, user)

    saved_posts_url = reverse('posts:saved')
    saved_posts_response = client.get(saved_posts_url)
    assert saved_posts_response.status_code == status.HTTP_200_OK
    saved_posts_count = saved_posts_response.data['count']
    assert saved_posts_count == models.Save.objects.filter(user=user).count()