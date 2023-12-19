import pytest

from posts import models
from posts.tests import conftest as posts_conftest
from backend import conftest as users_conftest


@pytest.mark.django_db
def test_save_model(
    create_post: posts_conftest.CreatePostFixture, 
    create_user: users_conftest.CreateUserFixture
):

    user = create_user()
    post = create_post()  # type: ignore

    save = models.SavedPost.objects.create(post=post, user=user)

    assert str(save) == f"post {post.id} was saved"

    assert post.savedpost_set.count() == 1