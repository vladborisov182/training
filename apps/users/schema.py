from graphene import ObjectType, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Trainer, User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ["id", "username"]
        interfaces = (relay.Node,)


class TrainerNode(DjangoObjectType):
    class Meta:
        model = Trainer
        filter_fields = {"name": ["exact", "icontains", "istartswith"]}
        interfaces = (relay.Node,)


class UserQuery(ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)


class TrainerQuery(ObjectType):
    all_trainers = DjangoFilterConnectionField(TrainerNode)
    all_trainers_users = DjangoFilterConnectionField(UserNode)
