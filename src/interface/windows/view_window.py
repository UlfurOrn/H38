from uuid import UUID

from pydantic import BaseModel

from interface.windows.window import Button, Window
from logic.helpers import InfoModel
from logic.logic.employee_logic import EmployeeInfo
from logic.logic_api import api


class Field(BaseModel):
    name: str
    field: str


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
            print(f"|{field.name:>16}: {value:<29}|")


class EmployeeViewWindow(ViewWindow):
    title = "View Employee"
    info: EmployeeInfo
    buttons = [Button(letter="b", description="back", function=None)]

    def window_setup(self) -> None:
        self.info = api.employees.get(self.model_id)
