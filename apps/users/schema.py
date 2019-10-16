import graphene
from graphene_django.types import DjangoObjectType

from .models import Trainer, User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class TrainerType(DjangoObjectType):
    class Meta:
        model = Trainer


class TrainerQuery(object):
    trainer = graphene.Field(TrainerType, id=graphene.Int(), name=graphene.String())
    all_trainers = graphene.List(TrainerType)
    all_trainers_users = graphene.List(UserType)

    def resolve_trainer(self, info, **kwargs):
        pk = kwargs.get("id")
        name = kwargs.get("name")
        if pk:
            return Trainer.objects.get(pk=pk)
        if name:
            return Trainer.objects.get(name=name)
        return None

    def resolve_all_trainers(self, info, **kwargs):
        return Trainer.objects.all()

    def resolve_all_trainers_users(self, info, **kwargs):
        return Trainer.objects.select_related("users").all()


class UserQuery(object):
    user = graphene.Field(UserType, id=graphene.Int())
    all_users = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        pk = kwargs.get("id")
        if pk:
            return User.objects.get(pk=pk)
        return None

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
