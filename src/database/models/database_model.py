from __future__ import annotations

import os
from csv import DictReader, DictWriter
from typing import Optional, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel

from utils.exceptions import NotFoundException


class DatabaseModel(BaseModel):
    _HEADERS = None
    _PATH = "/database/data/"
    _FILENAME = None

    id: Optional[UUID] = None

    @classmethod
    def __get_filepath(cls) -> str:
        if cls._FILENAME is None:
            raise Exception(f"Specify FILENAME for class {cls.__name__}")

        return f"{os.curdir}{cls._PATH}{cls._FILENAME}"

    @classmethod
    def read(cls) -> list[Model]:
        filepath = cls.__get_filepath()
        with open(filepath, "r", encoding="utf-8") as file_object:
            reader = DictReader(file_object)
            data = [cls.deserialize(model) for model in reader]

        return data

    @classmethod
    def save(cls, data: list[Model]) -> None:
        filepath = cls.__get_filepath()
        with open(filepath, "w", encoding="utf-8") as file_object:
            writer = DictWriter(file_object, cls._HEADERS)
            writer.writeheader()
            for model in data:
                writer.writerow(cls.serialize(model))

    def create(self) -> Model:
        if self.id is not None:
            raise Exception(f'{self.__class__} with ID "{self.id}" has already been created')

        self.id = uuid4()

        data = self.read()
        data.append(self)

        self.save(data)
        return self

    def update(self) -> Model:
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
    def all(cls) -> list[Model]:
        return cls.read()

    @classmethod
    def _get_model(cls, models: list[DatabaseModel], model_id: UUID) -> Model:
        for model in models:
            if model.id == model_id:
                return model

        raise NotFoundException(f'{cls.__name__} with ID "{model_id}" does not exist')

    @classmethod
    def many(cls, model_ids: list[UUID]) -> list[Model]:
        data = cls.read()
        return [cls._get_model(data, model_id) for model_id in model_ids]

    @classmethod
    def get(cls, model_id: UUID) -> Model:
        data = cls.read()
        return cls._get_model(data, model_id)

    @classmethod
    def serialize(cls, model: Model) -> dict:
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data: dict) -> Model:
        raise NotImplementedError()

    @classmethod
    def _optional(cls, data: dict, field: str) -> None:
        data[field] = None if data[field] == "" else data[field]


# Type hint for any subclass of DatabaseModel
Model = TypeVar("Model", bound=DatabaseModel)
