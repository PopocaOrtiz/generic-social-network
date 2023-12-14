import pytest

from market import models
from users.tests import conftest as conftest_users


@pytest.mark.django_db
def test_job_model(create_user: conftest_users.CreateUserFixture):

    user = create_user()

    job = models.Job.objects.create(name='test job', user=user)

    assert str(job) == f"test job"