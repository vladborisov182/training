import factory

from .models import User, Trainer


class TrainerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trainer

    name = factory.Faker("first_name")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("first_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    user_code = "code"
    user_text = "text"
    trainer = factory.SubFactory(TrainerFactory)
