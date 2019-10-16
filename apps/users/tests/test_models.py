import pytest
from graphene.test import Client

from apps.users.models import User
from conf.schema import schema

pytestmark = pytest.mark.django_db


@pytest.fixture()
def schema_client():
    return Client(schema)


def test_user_str_method():
    assert str(User(email="email@email.com")) == "email@email.com"


def test_get_list_of_trainers(schema_client, user_factory, trainer_factory):
    trainers_list = trainer_factory.create_batch(3)
    for trainer in trainers_list:
        user_factory.create_batch(2, trainer=trainer)

    response_content = schema_client.execute(
        """
        query {
            allTrainers {
                id
                name
                users {
                    id
                }
            }
        }
        """
    )
    assert not response_content.get("errors")

    returned_trainers = response_content["data"]["allTrainers"]
    all_trainers_names = [x.name for x in trainers_list]
    retuned_trainers_names = [x["name"] for x in returned_trainers]

    assert set(all_trainers_names) == set(retuned_trainers_names)
    assert len(all_trainers_names) == len(retuned_trainers_names)

    for trainer in returned_trainers:
        assert len(trainer["users"]) == 2


def test_get_all_users(schema_client, user_factory):
    users = user_factory.create_batch(5)

    response_content = schema_client.execute(
        """
        query {
            allUsers {
                username
            }
        }
        """
    )
    assert not response_content.get("errors")

    returned_users = response_content["data"]["allUsers"]
    all_users_user_names = [x.username for x in users]
    retuned_users_user_names = [x["username"] for x in returned_users]

    assert set(all_users_user_names) == set(retuned_users_user_names)
    assert len(all_users_user_names) == len(retuned_users_user_names)


def test_get_user_by_id(schema_client, user_factory):
    user = user_factory()

    response_content = schema_client.execute(
        """
            query user($id: Int!){
                user(id: $id) {
                    id
                    username
                }
            }
        """,
        variables={"id": user.id},
    )
    assert not response_content.get("errors")

    returned_user = response_content["data"]

    assert len(returned_user) == 1
    assert returned_user["user"]["username"] == user.username


def test_get_trainer_by_id(schema_client, trainer_factory):
    trainer = trainer_factory()

    response_content = schema_client.execute(
        """
            query trainer($id: Int!){
                trainer(id: $id) {
                    id
                    name
                }
            }
        """,
        variables={"id": trainer.id},
    )
    assert not response_content.get("errors")

    returned_user = response_content["data"]

    assert len(returned_user) == 1
    assert returned_user["trainer"]["name"] == trainer.name


def test_get_trainer_by_name(schema_client, trainer_factory):
    trainer = trainer_factory()

    response_content = schema_client.execute(
        """
            query trainer($name: String!){
                trainer(name: $name) {
                    name
                    name
                }
            }
        """,
        variables={"name": trainer.name},
    )
    assert not response_content.get("errors")

    returned_user = response_content["data"]

    assert len(returned_user) == 1
    assert returned_user["trainer"]["name"] == trainer.name
