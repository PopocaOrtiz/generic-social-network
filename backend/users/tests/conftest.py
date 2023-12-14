from os import path
from typing import Callable, Generator, Optional

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

from users.models import UserType


@pytest.fixture
def image_file():

    file_path = path.join(path.dirname(path.abspath(__file__)), 'data/image.png')

    with open(file_path, 'rb') as file:
        yield SimpleUploadedFile('image.png', file.read(), content_type='image/png')


@pytest.fixture
def s3_upload_in_memory_file(mocker):

    upload_in_memory_file = mocker.patch('aws.facades.s3.S3.upload_in_memory_file')
    upload_in_memory_file.return_value = 'https://bucket.aws.com/image.png'

    yield upload_in_memory_file


CreateUserFixture = Callable[[], UserType]


@pytest.fixture
def create_user() -> Generator[CreateUserFixture, None, None]:

    fake = Faker()

    def create() -> UserType:
        email = fake.email()
        username = fake.user_name()
        return get_user_model().objects.create(email=email, username=username) # type: ignore
    
    yield create


@pytest.fixture
def api_client():

    client = APIClient()

    yield client


@pytest.fixture
def auth_client(create_user: CreateUserFixture):
    """
    returns a function that returns an api client and the (forced) authenticated user
    """

    def get():
        user = create_user()

        client = APIClient()
        client.force_authenticate(user)

        return client, user

    yield get