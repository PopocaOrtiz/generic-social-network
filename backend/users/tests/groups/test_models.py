import pytest

from users import models
from backend import conftest


@pytest.mark.django_db
def test_group_model(create_user: conftest.CreateUserFixture):

    group = models.Group.objects.create(name='test group')

    assert str(group) == 'test group'

    user1 = create_user()
    group.users.add(user1)

    assert group.users.count() == 1