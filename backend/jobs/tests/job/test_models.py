import pytest
from django.core.exceptions import ValidationError

from jobs import models
from backend import conftest as conftest_users


@pytest.mark.django_db
def test_job_model(create_user: conftest_users.CreateUserFixture):

    user = create_user()

    job = models.Job.objects.create(title='test job', user=user)

    assert str(job) == f"test job"


@pytest.mark.django_db
def test_cant_apply_own_job(create_user: conftest_users.CreateUserFixture):

    user = create_user()

    job = models.Job.objects.create(title='test job', user=user)

    with pytest.raises(ValidationError):
        models.JobApplication.objects.create(job=job, user=user)    