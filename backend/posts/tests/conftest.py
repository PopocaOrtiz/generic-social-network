from typing import Callable

from posts import models


CreatePostFixture = Callable[[], models.Post]