import pytest

from users import models
from users.tests import conftest


@pytest.mark.xfail
@pytest.mark.django_db
def test_group_model(create_user: conftest.CreateUserFixture):

    group = models.Group.objects.create(name='test group')

    assert str(group) == 'test group'

    user1 = create_user()
    group.users_set.add(user1)

    assert group.users_set.count() == 1