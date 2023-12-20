import pytest
from django.urls import reverse
from rest_framework import status

from posts import models


@pytest.fixture
def create_report(create_user):
    def _create(post, user=None, type="spam"):

        if not user:
            user = create_user()

        report = models.Report.objects.create(post=post, user=user, type=type)
        return report
    return _create


@pytest.mark.django_db
def test_send_report(auth_client, create_post):

    client, _ = auth_client()
    
    post = create_post()

    url = reverse("posts:post-reports", args=[post.id])

    response = client.post(url, {"type": "SPAM", "comment": ""})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["type"] == "SPAM"
    assert models.Post.objects.get(id=post.id).reports.count() == 1


@pytest.mark.django_db
def test_fetch_report_list(auth_client, create_post, create_report):
    
    client, user = auth_client()

    post = create_post(user=user)
    create_report(post=post)
    create_report(post=post)

    url = reverse("posts:post-reports", args=[post.id])
    
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2