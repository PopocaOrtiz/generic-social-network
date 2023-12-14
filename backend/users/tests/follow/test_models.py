import pytest

from users import models
from users.tests import conftest


@pytest.mark.xfail
@pytest.mark.django_db
def test_follow_model(create_user: conftest.CreateUserFixture):

    follow = models.Follow.objects.create(
        user1 := create_user(),
        user2 := create_user()
    )

    assert str(follow) == f"{user1.id} follows {user2.id}"