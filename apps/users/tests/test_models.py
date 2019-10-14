import json

import pytest
from graphene_django.utils.testing import GraphQLTestCase

from apps.users.factories import UserFactory, TrainerFactory
from apps.users.models import User
from conf.schema import schema

pytestmark = pytest.mark.django_db


class TestModels(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_user_str_method(self):
        assert str(User(email="email@email.com")) == "email@email.com"

    def test_get_list_of_trainers(self):
        trainers_list = TrainerFactory.create_batch(3)
        for trainer in trainers_list:
            UserFactory.create_batch(2, trainer=trainer)

        response = self.query(
            """
            query {
                allTrainers {
                    name
                    users {
                        username
                    }
                }
            }
            """,
            op_name="Trainer",
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        returned_trainers = content["data"]["allTrainers"]
        all_trainers_names = [x.name for x in trainers_list]
        retuned_trainers_names = [x["name"] for x in returned_trainers]

        self.assertEqual(set(all_trainers_names), set(retuned_trainers_names))
        self.assertEqual(len(all_trainers_names), len(retuned_trainers_names))

        for trainer in returned_trainers:
            self.assertEqual(len(trainer["users"]), 2)

    def test_get_all_users(self):
        users = UserFactory.create_batch(5)

        response = self.query(
            """
            query {
                allUsers {
                    username
                }
            }
            """,
            op_name="User",
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        returned_users = content["data"]["allUsers"]
        all_users_user_names = [x.username for x in users]
        retuned_users_user_names = [x["username"] for x in returned_users]

        self.assertEqual(set(all_users_user_names), set(retuned_users_user_names))
        self.assertEqual(len(all_users_user_names), len(retuned_users_user_names))
