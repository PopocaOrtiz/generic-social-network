import pytest
from rest_framework import status
from django.urls import reverse

from posts import models


@pytest.fixture
def save_post():
    def create_save(post, user):
        save = models.SavedPost.objects.create(post=post, user=user)
        return save
    return create_save


@pytest.mark.django_db
def test_save_post(auth_client, create_post):

    client, user = auth_client()

    post = create_post()

    url = reverse('posts:post-save', args=[post.id])

    response = client.post(url)

    assert response.status_code == status.HTTP_201_CREATED

    user_saved_posts = models.SavedPost.objects.filter(user=user)

    assert user_saved_posts.count() == 1
    assert user_saved_posts.filter(post=post).exists()


@pytest.mark.django_db
def test_fetch_saved_posts(auth_client, create_post, save_post):

    client, user = auth_client()

    save_post(post1 := create_post(), user)
    save_post(post2 := create_post(), user)
    create_post()

    queryset = models.SavedPost.objects.filter(user=user)

    url = reverse('posts:post-saved')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    
    assert queryset.count() == 2
    assert queryset.filter(post__id__in=[post1.id, post2.id]).count() == 2