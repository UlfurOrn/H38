from __future__ import annotations

from csv import DictReader, DictWriter

from pydantic import BaseModel


class DatabaseModel(BaseModel):
    _HEADERS = None
    _PATH = "../../database/data/"
    _FILENAME = None

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

    @classmethod
    def serialize(cls, model: DatabaseModel) -> dict:
        raise NotImplementedError()

    @classmethod
    def deserialize(cls, data: dict) -> DatabaseModel:
        raise NotImplementedError()
