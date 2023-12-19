import pytest
from django.urls import reverse
from rest_framework import status
from jobs.models import Job

@pytest.fixture
def create_job(create_user):
    def _create_job(user=None):
        if user is None:
            user = create_user()
        job = Job.objects.create(user=user, title="Test Job", description="This is a test job")
        return job
    return _create_job


@pytest.mark.django_db
def test_fetch_job_list(api_client, create_job):

    for _ in range(3):
        create_job()
    
    url = reverse("jobs:jobs-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.django_db
def test_create_job(auth_client):

    client, user = auth_client()

    url = reverse("jobs:jobs-list")

    data = {
        "title": "Test Job",
        "description": "This is a test job"
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Job.objects.filter(title="Test Job", description="This is a test job").exists()