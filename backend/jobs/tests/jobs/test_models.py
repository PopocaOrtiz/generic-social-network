import pytest
from django.core.exceptions import ValidationError

from market import models
from users.tests import conftest as conftest_users


@pytest.mark.xfail
@pytest.mark.django_db
def test_job_model(create_user: conftest_users.CreateUserFixture):

    user = create_user()

    job = models.Job.objects.create(title='test job', user=user)

    assert str(job) == f"test job"


@pytest.mark.xfail
@pytest.mark.django_db
def test_cant_apply_own_job(create_user: conftest_users.CreateUserFixture):

    user = create_user()

    job = models.Job.objects.create(title='test job', user=user)

    with pytest.raises(ValidationError):

        job.applicants_set.add(user)
