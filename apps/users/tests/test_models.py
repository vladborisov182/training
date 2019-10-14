import json

import pytest
from graphene_django.utils.testing import GraphQLTestCase

from apps.users.factories import UserFactory, TrainerFactory
from apps.users.models import User, Trainer
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
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        returned_trainers = content["data"]["allTrainers"]["edges"]
        all_trainers_names = [x.name for x in trainers_list]
        retuned_trainers_names = [x["node"]["name"] for x in returned_trainers]

        self.assertEqual(set(all_trainers_names), set(retuned_trainers_names))
        self.assertEqual(len(all_trainers_names), len(retuned_trainers_names))

        for trainer in returned_trainers:
            self.assertEqual(len(trainer["node"]["users"]["edges"]), 2)

    def test_get_all_users(self):
        users = UserFactory.create_batch(5)

        response = self.query(
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
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        returned_users = content["data"]["allUsers"]["edges"]
        all_users_user_names = [x.username for x in users]
        retuned_users_user_names = [x["node"]["username"] for x in returned_users]

        self.assertEqual(set(all_users_user_names), set(retuned_users_user_names))
        self.assertEqual(len(all_users_user_names), len(retuned_users_user_names))

    def test_get_user_by_id(self):
        user = UserFactory()

        response = self.query(
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
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        returned_user = content["data"]["allUsers"]["edges"]

        self.assertEqual(len(returned_user), 1)
        self.assertEqual(returned_user[0]["node"]["username"], user.username)

    def test_get_user_by_username(self):
        user = UserFactory()

        response = self.query(
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
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        returned_user = content["data"]["allUsers"]["edges"]

        self.assertEqual(len(returned_user), 1)
        self.assertEqual(returned_user[0]["node"]["username"], user.username)

    def test_trainers_by_name(self):
        trainers = TrainerFactory.create_batch(5)

        for trainer in trainers:
            trainer_name = trainer.name
            response = self.query(
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
            self.assertResponseNoErrors(response)

            content = json.loads(response.content)
            returned_trainers = content["data"]["allTrainers"]["edges"]

            self.assertEqual(
                len(returned_trainers),
                Trainer.objects.filter(name__icontains=trainer_name).count(),
            )
            self.assertEqual(returned_trainers[0]["node"]["name"], trainer_name)
