from uuid import UUID

from pydantic import BaseModel

from interface.extra import Field
from interface.window_types.window import Button, Window
from logic.api import api
from logic.helpers import InfoModel
from logic.logic.employee_logic import EmployeeInfo


class ViewWindow(Window):
    model_id: UUID
    info: InfoModel
    fields: list[Field]

    def window_setup(self) -> None:
        raise NotImplementedError()

    def display(self) -> None:
        self.boundary()
        self.empty()
        self.display_info()
        self.empty()
        self.boundary()

    def display_info(self) -> None:
        for field in self.fields:
            value = self.info.get(field.field)
            print(f"|{field.name:>16}: {value:<30}|")
