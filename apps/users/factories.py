import factory

from .models import User, Trainer


class TrainerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trainer

    name = factory.Sequence(lambda n: "trainer_{}".format(n))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Sequence(lambda n: "username_{}".format(n))
    first_name = factory.Sequence(lambda n: "first_name_{}".format(n))
    last_name = factory.Sequence(lambda n: "last_name_{}".format(n))
    user_code = "code"
    user_text = "text"
    trainer = factory.SubFactory(TrainerFactory)
