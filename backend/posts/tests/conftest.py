from typing import Callable, Optional

import pytest

from posts import models
from users.models import UserType


CreatePostFixture = Callable[[Optional[UserType]], models.Post]


@pytest.fixture
def create_post(create_user) -> CreatePostFixture:
    def _create_post(user = None):

        if user is None:
            user = create_user()

        return models.Post.objects.create(author=user, content='post content')

    return _create_post