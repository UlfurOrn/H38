from uuid import UUID

from interface.extra import Button, Field
from interface.window_types.window import Window
from logic.helpers import InfoModel
from logic.api import api
from logic.logic.employee_logic import EmployeeInfo, EmployeeItem


class SearchWindow(Window):
    info: dict
    field: Field
    search_type: str
    item: str

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="s", description="submit", function=self.submit),
            Button(letter="c", description="clear", function=self.clear),
            Button(letter="b", description="back", function=self.back),
        ]

    def window_setup(self) -> None:
        self.info = {}

    def setup(self) -> None:
        if self.info.get(self.field.field) is None:
            self.hide_button("s")  # Submit button
            self.hide_button("c")  # Clear button

    def display(self) -> None:
        self.boundary()
        self.empty()
        self.centered(f"# Please enter {self.search_type} for {self.item}")
        self.empty()
        self.display_info()
        self.empty()
        self.boundary()

    def display_info(self) -> None:
        value = self.info.get(self.field.field)
        value = value or ""

        print(f"|{self.field.name:>16}: {value:<30}|")

    def parse_input(self, data: str) -> None:
        if data:
            self.info[self.field.field] = data

    def get_input(self, text: str = "Enter Command: ") -> str:
        return super().get_input(text=text)

    def submit(self) -> UUID:
        raise NotImplementedError()

    def clear(self) -> None:
        self.info[self.field.field] = None



class EmployeeSearchWindow(SearchWindow):
    
    title = "Search Employee"
    search_type = "ssn"
    item = "employee"

    field = Field(name="SSN", field="ssn", requied = True)

    def submit(self) -> UUID:
        employee = api.employees.all(search = self.value)   # -> Paginator
        
        #employee_id = api.employees.get(employee.ssn) 




# +-----------------------------------------------+
# |                Search Employee                |
# +-----------------------------------------------+
# |                                               |
# |      # Please enter SSN for employee          |
# |                                               |
# |               ssn:  1909992979                |
# |                                               |
# |                                               |
# |                                               |
# |                                               |
# |                                               |
# +-----------------------------------------------+
# | s: submit         c: clear            b: back |
# +-----------------------------------------------+