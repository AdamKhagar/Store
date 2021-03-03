from django.contrib.auth import get_user_model
from factory import SubFactory, Sequence, PostGenerationMethodCall
from factory.django import DjangoModelFactory


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = Sequence(lambda n: f'user#{n}')
    name = Sequence(lambda n: f'name#{n}')
    lastname = Sequence(lambda n: f'lastname#{n}')
    email = Sequence(lambda n: f'email#{n}@gmail.com')
    password = PostGenerationMethodCall('set_password', 'qwerty123')


