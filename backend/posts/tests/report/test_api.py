import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def create_report():
    def _create(post, user, reason="spam"):
        report = models.Report.objects.create(post=post, user=user, reason=reason)
        return report
    return _create


@pytest.mark.django_db
@pytest.mark.xfail
def test_report_post(auth_client, create_post):
    user, client = auth_client()
    post = create_post(user)
    url = reverse("posts:post-reports", args=[post.id])
    response = client.post(url, {"reason": "spam"})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
@pytest.mark.xfail
def test_fetch_report_list(auth_client, create_post, create_report):
    
    user, client = auth_client()
    post = create_post(user)
    report = create_report(post, user)

    url = reverse("posts:post-reports", args=[post.id])
    
    response = client.get(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()) == 1
