import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from users import models
from backend import conftest


@pytest.mark.django_db
def test_follow_model(create_user: conftest.CreateUserFixture):

    user1 = create_user()
    user2 = create_user()

    follow = models.Follow.objects.create(follower=user1, followed=user2)

    assert str(follow) == f"{user1.id} follows {user2.id}"


@pytest.mark.django_db
def test_cant_follow_twice(create_user: conftest.CreateUserFixture):

    follower = create_user()
    followed = create_user()

    models.Follow.objects.create(follower=follower, followed=followed)

    assert followed.followers.count() == 1

    with pytest.raises(IntegrityError):
        models.Follow.objects.create(follower=follower, followed=followed)


@pytest.mark.django_db
def test_cant_follow_yourself(create_user: conftest.CreateUserFixture):

    user = create_user()

    with pytest.raises(ValidationError):
        models.Follow.objects.create(follower=user, followed=user)