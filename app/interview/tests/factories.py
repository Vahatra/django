from dataclasses import dataclass

from faker import Faker

from app.interview.serializers import InterviewSerializer
from app.utils.factory import SerializerFactory

fake = Faker()


@dataclass
class InterviewSerializerFactory(SerializerFactory):
    serializer_class = InterviewSerializer

    def __post_init__(self):
        pass
