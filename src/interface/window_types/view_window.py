from uuid import UUID

from interface.extra import Field, WindowState
from interface.window_types.window import Button, Window
from logic.helpers import InfoModel


class ViewWindow(Window):
    info: InfoModel
    fields: list[Field]

    def __init__(self, model_id: UUID, window_state: WindowState = WindowState.Normal):
        self.model_id = model_id
        self.window_state = window_state

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="u", description="update", function=self.update, supervisor=True),
            Button(letter="s", description="select", function=self.select),
            Button(letter="v", description="view", function=self.view),
            Button(letter="b", description="back", function=self.back),
        ]

    def window_setup(self) -> None:
        raise NotImplementedError()

    def window_state_setup(self) -> None:
        if self.window_state != WindowState.Normal:
            self.hide_button("u")
        if self.window_state != WindowState.Select:
            self.hide_button("s")
        if self.window_state != WindowState.Add:
            self.hide_button("+")

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
