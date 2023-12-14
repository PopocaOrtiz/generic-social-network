import pytest

from market import models
from users.tests import conftest as conftest_users


@pytest.mark.xfail
@pytest.mark.django_db
def test_ad_model(create_user: conftest_users.CreateUserFixture):

    user = create_user()

    ad = models.Ad.objects.create(title='test message', creator=user)

    assert str(ad) == f"{ad.title} by {user.full_name}"