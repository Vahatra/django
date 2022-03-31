from dataclasses import dataclass
from typing import Any, Sequence

from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from app.utils.factory import SerializerFactory
from app.utils.utils import slugify
from django.contrib.auth import get_user_model

from ..models import User
from ..serializers import UserSerializer

fake = Faker()


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


@dataclass
class UserSerializerFactory(SerializerFactory):
    serializer_class = UserSerializer
    username: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    email: str = None

    def __post_init__(self):
        if self.first_name is None or self.last_name is None:
            first_name = fake.first_name()
            last_name = fake.last_name()
            self.first_name = first_name
            self.last_name = last_name
            self.email = slugify(f"{first_name} {last_name}") + "@example.com"
        if self.username is None:
            self.username = User.objects.generate_username(first_name, last_name)
        if self.password is None:
            self.password = "pwdTest123*"
