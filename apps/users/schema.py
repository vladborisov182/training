import graphene
from graphene_django.types import DjangoObjectType

from .models import Trainer, User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class TrainerType(DjangoObjectType):
    class Meta:
        model = Trainer


class UserQuery(object):
    user = graphene.Field(UserType, id=graphene.Int(), username=graphene.String())
    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        identifier = kwargs.get("id")
        username = kwargs.get("username")

        if identifier:
            return User.objects.get(pk=identifier)
        if username:
            return User.objects.get(username=username)
        return None


class TrainerQuery(object):
    all_trainers = graphene.List(TrainerType)
    all_trainers_users = graphene.List(UserType)

    def resolve_all_trainers(self, info, **kwargs):
        return Trainer.objects.all()

    def resolve_all_trainers_users(self, info, **kwargs):
        return Trainer.objects.select_related("users").all()
