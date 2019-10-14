import graphene

from apps.users.schema import TrainerQuery, UserQuery


class Query(TrainerQuery, UserQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
