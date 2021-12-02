from uuid import UUID

from pydantic import BaseModel

from interface.window_types.window import Button, Window
from logic.api import api
from logic.helpers import InfoModel
from logic.logic.employee_logic import EmployeeInfo


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
            print(f"|{field.name:>16}: {value:<30}|")


class EmployeeViewWindow(ViewWindow):
    title = "View Employee"
    info: EmployeeInfo
    fields = [
        Field(name="Name", field="name"),
        Field(name="SSN", field="ssn"),
        Field(name="Address", field="address"),
        Field(name="Email", field="email"),
        Field(name="Home Phone", field="home_phone"),
        Field(name="Work Phone", field="work_phone"),
        Field(name="Location", field="location"),
    ]

    def window_setup(self) -> None:
        self.info = api.employees.get(self.model_id)

    def update(self) -> None:
        print("Update")

    buttons = [
        Button(letter="u", description="update", function=update),
        Button(letter="b", description="back", function=None),
    ]
