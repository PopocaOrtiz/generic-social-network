import pytest

from market import models
from users.tests import conftest as conftest_users


@pytest.mark.xfail
@pytest.mark.django_db
def test_product_model(create_user: conftest_users.CreateUserFixture):

    user = create_user()

    report = models.Product.objects.create(name='test product', user=user)

    assert str(report) == f"test product"