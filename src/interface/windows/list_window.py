from pydantic import BaseModel

from interface.windows.window import Window


class Column(BaseModel):
    name: str
    field: str
    size: int


class ListWindow(Window):
    columns = [
        Column(name="Name", field="name", size=20),
        Column(name="SSN", field="ssn", size=11),
        Column(name="Phone", field="work_phone", size=9),
    ]

    def header(self) -> None:
        boundary = self._get_boundary()

        for column in self.columns:
            pass
