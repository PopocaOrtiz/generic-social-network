import pytest

from market import models
from users.tests import conftest


@pytest.mark.django_db
def test_group_model(create_user: conftest.CreateUserFixture):

    product = models.Product.objects.create(name='test product')

    assert str(product) == 'test product'