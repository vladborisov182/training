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
    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()


class TrainerQuery(object):
    all_trainers = graphene.List(TrainerType)
    all_trainers_users = graphene.List(UserType)

    def resolve_all_trainers(self, info, **kwargs):
        return Trainer.objects.all()

    def resolve_all_trainers_users(self, info, **kwargs):
        return Trainer.objects.select_related("users").all()
