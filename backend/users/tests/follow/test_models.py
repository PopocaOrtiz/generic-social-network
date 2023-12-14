import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError

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


@pytest.mark.xfail
@pytest.mark.django_db
def test_cant_follow_twice(create_user: conftest.CreateUserFixture):

    follower = create_user()
    followed = create_user()

    models.Follow.objects.create(follower, followed)

    assert followed.followers_set.count() == 1

    with pytest.raises(IntegrityError, match="user .* is already following user .*"):
        models.Follow.objects.create(follower, followed)


@pytest.mark.xfail
@pytest.mark.django_db
def test_cant_follow_yourself(create_user: conftest.CreateUserFixture):

    user = create_user()

    with pytest.raises(ValidationError):
        models.Follow.objects.create(follower=user, following=user)