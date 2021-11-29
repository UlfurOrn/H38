from __future__ import annotations

from csv import DictReader, DictWriter
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from utils.exceptions import NotFoundException


class DatabaseModel(BaseModel):
    _HEADERS = None
    _PATH = "../../database/data/"
    _FILENAME = None

    id: Optional[UUID] = None

    @classmethod
    def __get_filepath(cls) -> str:
        if cls._FILENAME is None:
            raise Exception(f"Specify FILENAME for class {cls.__name__}")

        return f"{cls._PATH}{cls._FILENAME}"

    @classmethod
    def read(cls) -> list[DatabaseModel]:
        filepath = cls.__get_filepath()
        with open(filepath, "r") as file_object:
            reader = DictReader(file_object)
            data = [cls.deserialize(model) for model in reader]

        return data

    @classmethod
    def save(cls, data: list[DatabaseModel]) -> None:
        filepath = cls.__get_filepath()
        with open(filepath, "w") as file_object:
            writer = DictWriter(file_object, cls._HEADERS)
            writer.writeheader()
            for model in data:
                writer.writerow(cls.serialize(model))

    def create(self) -> DatabaseModel:
        if self.id is not None:
            raise Exception(f'{self.__class__} with ID "{self.id}" has already been created')

        self.id = uuid4()

        data = self.read()
        data.append(self)

        self.save(data)
        return self

    def update(self) -> DatabaseModel:
        if self.id is None:
            raise NotFoundException(f"{self.__class__} has not been created")

        data = self.read()

        for index, model in enumerate(data):
            if model.id == self.id:
                data[index] = self
                self.save(data)
                return self

        raise NotFoundException(f'{self.__class__} with ID "{self.id}" does not exist')

    @classmethod
    def serialize(cls, model: DatabaseModel) -> dict:
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data: dict) -> DatabaseModel:
        raise NotImplementedError()
