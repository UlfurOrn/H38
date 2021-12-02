from interface.extra import CreateField
from interface.window_types.view_window import Field
from interface.window_types.window import Button, Return, Window
from logic.api import api
from logic.logic.employee_logic import EmployeeCreate


class CreateWindow(Window):
    info: dict = {}
    fields: list[CreateField]
    current: int

    def window_setup(self) -> None:
        self.current = 0

    def setup(self) -> None:
        submit_button = self.get_button("s")

        for field in self.fields:
            if field.required and self.info.get(field.field) is None:
                submit_button.hide = True
                break

        submenu_button = self.get_button("f")
        if not self.fields[self.current].submenu:
            submenu_button.hide = True

    def display(self) -> None:
        self.boundary()
        self.empty()
        self.display_info()
        self.empty()
        self.boundary()

    def display_info(self) -> None:
        for field in self.fields:
            value = self.info.get(field.field)
            value = value or ""
            if field == self.fields[self.current]:
                value = value[:7] + " <---"
            print(f"|{field.name:>16}: {value:<30}|")

    def parse_input(self, data: str) -> None:
        if data:
            field = self.fields[self.current]
            self.info[field.field] = data

        self.current = (self.current + 1) % len(self.fields)
