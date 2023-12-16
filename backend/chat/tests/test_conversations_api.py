import pytest
from django.urls import reverse
from rest_framework import status

from chat import models


@pytest.fixture
def create_message(create_user):
    def _create_message(sender=None, receiver=None):
        if receiver is None:
            receiver = create_user()
        return models.Message.objects.create(sender=sender, receiver=receiver)
    return _create_message


@pytest.mark.django_db
@pytest.mark.xfail
def test_fetch_conversations_list(auth_client, create_message):
    
    client, user = auth_client()

    create_message(sender=user)
    create_message(sender=user)
    create_message(sender=user)

    url = reverse("chat:conversations")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
