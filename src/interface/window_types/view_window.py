from uuid import UUID

from interface.extra import Field
from interface.window_types.window import Button, Window
from logic.helpers import InfoModel
from utils.verification import Verification


class ViewWindow(Window):
    info: InfoModel
    fields: list[Field]

    def __init__(self, model_id: UUID):
        self.model_id = model_id

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="u", description="update", function=self.update, supervisor=True),
            Button(letter="s", description="select", function=self.select),
            Button(letter="v", description="view", function=self.view),
            Button(letter="b", description="back", function=self.back),
        ]

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
            value = value or ""
            print(f"|{field.name:>16}: {value:<30}|")

    def update(self) -> None:
        raise NotImplementedError()

    def select(self) -> InfoModel:
        raise NotImplementedError()

    def view(self) -> None:
        raise NotImplementedError()
