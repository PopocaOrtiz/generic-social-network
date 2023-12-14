import pytest

from posts import models
from users.tests import conftest as conftest_users
from posts.tests import conftest


@pytest.mark.django_db
def test_report_model(create_post: conftest.CreatePostFixture, create_user: conftest_users.CreateUserFixture):


    user = create_user()
    post = create_post()

    report = models.Report.objects.create(post=post, user=user)

    assert str(report) == f"post {post.id} was reported for {report.type}"

    assert post.reports_set.count() == 1


@pytest.mark.django_db
def test_save_model(create_post: conftest.CreatePostFixture, create_user: conftest_users.CreateUserFixture):


    user = create_user()
    post = create_post()

    save = models.Save.objects.create(post=post, user=user)

    assert str(save) == f"post {post.id} was saved"

    assert post.saves_set.count() == 1