from os import path

import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def api_client():

    client = APIClient()

    yield client


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
