import pytest
from graphene.test import Client

from apps.users.factories import TrainerFactory, UserFactory
from apps.users.models import Trainer, User
from conf.schema import schema

pytestmark = pytest.mark.django_db


@pytest.fixture()
def schema_client():
    return Client(schema)


def test_user_str_method():
    assert str(User(email="email@email.com")) == "email@email.com"


def test_get_list_of_trainers(schema_client):
    trainers_list = TrainerFactory.create_batch(3)
    for trainer in trainers_list:
        UserFactory.create_batch(2, trainer=trainer)

    response_content = schema_client.execute(
        """
        query {
            allTrainers {
                edges {
                    node {
                        id,
                        name
                        users {
                            edges {
                                node {
                                    username
                                }
                            }
                        }
                    }
                }
            }
        }
        """,
        op_name="Trainer",
    )
    assert not response_content.get("errors")

    returned_trainers = response_content["data"]["allTrainers"]["edges"]
    all_trainers_names = [x.name for x in trainers_list]
    retuned_trainers_names = [x["node"]["name"] for x in returned_trainers]

    assert set(all_trainers_names) == set(retuned_trainers_names)
    assert len(all_trainers_names) == len(retuned_trainers_names)

    for trainer in returned_trainers:
        assert len(trainer["node"]["users"]["edges"]) == 2


def test_get_all_users(schema_client):
    users = UserFactory.create_batch(5)

    response_content = schema_client.execute(
        """
        query {
            allUsers {
                edges {
                    node {
                        username
                    }
                }
            }
        }
        """,
        op_name="User",
    )
    assert not response_content.get("errors")

    returned_users = response_content["data"]["allUsers"]["edges"]
    all_users_user_names = [x.username for x in users]
    retuned_users_user_names = [x["node"]["username"] for x in returned_users]

    assert set(all_users_user_names) == set(retuned_users_user_names)
    assert len(all_users_user_names) == len(retuned_users_user_names)


def test_get_user_by_id(schema_client):
    user = UserFactory()

    response_content = schema_client.execute(
        f"""
        query{{
            allUsers(id: {user.id}) {{
                edges {{
                    node {{
                        username
                    }}
                }}
            }}
        }}
        """,
        op_name="allUsers",
    )
    assert not response_content.get("errors")

    returned_user = response_content["data"]["allUsers"]["edges"]

    assert len(returned_user) == 1
    assert returned_user[0]["node"]["username"] == user.username


def test_get_user_by_username(schema_client):
    user = UserFactory()

    response_content = schema_client.execute(
        f"""
        query{{
            allUsers(username: "{user.username}") {{
                edges {{
                    node {{
                        username
                    }}
                }}
            }}
        }}
        """,
        op_name="allUsers",
    )
    assert not response_content.get("errors")

    returned_user = response_content["data"]["allUsers"]["edges"]

    assert len(returned_user) == 1
    assert returned_user[0]["node"]["username"] == user.username


def test_trainers_by_name(schema_client):
    trainers = TrainerFactory.create_batch(5)

    for trainer in trainers:
        trainer_name = trainer.name
        response_content = schema_client.execute(
            f"""
            query{{
                allTrainers(name_Icontains: "{trainer_name}") {{
                    edges {{
                        node {{
                            name
                        }}
                    }}
                }}
            }}
            """,
            op_name="allTrainers",
        )
        assert not response_content.get("errors")

        returned_trainers = response_content["data"]["allTrainers"]["edges"]

        assert (
            len(returned_trainers)
            == Trainer.objects.filter(name__icontains=trainer_name).count()
        )
        assert returned_trainers[0]["node"]["name"] == trainer_name
