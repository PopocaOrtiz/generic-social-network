import pytest

from market import models
from users.tests import conftest as conftest_users


@pytest.mark.xfail
@pytest.mark.django_db
def test_message_model(create_user: conftest_users.CreateUserFixture):

    user1 = create_user()
    user2 = create_user()

    message = models.Message.objects.create(name='test message', sender=user1, receiver=user2)

    assert str(message) == f"{message.id}"