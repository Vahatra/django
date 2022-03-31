from dataclasses import asdict, dataclass
from typing import Dict

from rest_framework.serializers import ModelSerializer


@dataclass
class SerializerFactory:
    serializer_class = None
    __instance = None

    def create(self, context: Dict = None):
        if self.__instance is None:
            data = asdict(self)
            data.pop("__instance", None)
            data.pop("_Factory__instance", None)
            # remove item with none value
            filtered_data = {k: v for k, v in data.items() if v is not None}
            if context is None:
                serializer: ModelSerializer = self.serializer_class(data=filtered_data)
            else:
                serializer: ModelSerializer = self.serializer_class(
                    data=filtered_data, context=context
                )
            serializer.is_valid(raise_exception=True)
            self.__instance = serializer.save()

        return self.__instance

    def update(self, data: Dict):
        serializer: ModelSerializer = self.serializer_class(
            self.__instance,
            data=data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        self.__instance = serializer.save()

        return self.__instance

    def get_data(self):
        if self.__instance:
            return self.serializer_class(instance=self.__instance).data

    def get_instance(self):
        return self.__instance
