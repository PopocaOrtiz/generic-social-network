import pytest

from posts.tests import conftest as posts_conftest
from users.tests import conftest as users_conftest


@pytest.mark.xfail
@pytest.mark.django_db
def test_save_model(
    create_post: posts_conftest.CreatePostFixture, 
    create_user: users_conftest.CreateUserFixture
):


    user = create_user()
    post = create_post()

    save = models.Save.objects.create(post=post, user=user)

    assert str(save) == f"post {post.id} was saved"

    assert post.saves_set.count() == 1