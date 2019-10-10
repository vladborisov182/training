import pytest

from apps.users.models import User
from rest_framework import status
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


def test_user_str_method():
    assert str(User(email="email@email.com")) == "email@email.com"


def get_list_of_users(client, user_factory):
    user_factory.create_batch(10)
    response = client.get(reverse("url_name"))
    assert response.status_code == status.HTTP_200_OK

    data = response.data
    returned_ids = [x["id"] for x in data]

    assert len(returned_ids) == 10

    list_of_fields = [
        "email",
        "username",
        "first_name",
        "last_name",
        "user_code",
        "user_text",
        "trainer",
    ]
    for user in User.objects.all().order_by("date_joined"):
        for field in list_of_fields:
            if field == "trainer":
                assert getattr(user, f"{field}__name") == data[field]["name"]
            else:
                assert getattr(user, field) == data[field]
