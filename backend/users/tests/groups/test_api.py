import pytest
from django.urls import reverse
from rest_framework import status

from users.models import Group


@pytest.fixture
def group():
    group = Group.objects.create(name='Test Group')
    yield group
    group.delete()


@pytest.mark.django_db
@pytest.mark.xfail
def test_join_group(auth_client):
    client, _ = auth_client()
    url = reverse('users:join-group')
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_201_CREATED