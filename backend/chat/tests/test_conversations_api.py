import pytest
from faker import Faker
from django.urls import reverse
from rest_framework import status

from chat import models


@pytest.fixture
def create_message(create_user):
    def _create_message(sender=None, receiver=None, message=None):

        if sender is None:
            sender = create_user()
            
        if receiver is None:
            receiver = create_user()

        if message is None:
            message = Faker().sentence()

        return models.Message.objects.create(sender=sender, receiver=receiver, message=message)
    return _create_message


@pytest.mark.django_db
def test_fetch_conversations_list(auth_client, create_message):
    
    client, user = auth_client()

    create_message(sender=user)
    create_message(receiver=user)

    # conversation with two messages
    msg = create_message(sender=user)
    create_message(sender=user, receiver=msg.receiver)

    url = reverse("chat:conversations")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
