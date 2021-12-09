from uuid import UUID
from interface.extra import WindowState

from interface.extra import Field
from interface.window_types.window import Button, Window
from logic.helpers import InfoModel


class ViewWindow(Window):
    info: InfoModel
    fields: list[Field]

    def __init__(self, model_id: UUID, window_state: WindowState):
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

    def hide_buttons(self) -> None:
        if self.window_state == WindowState.Normal:
            self.hide_button("a")
            self.hide_button("s")
        elif self.window_state == WindowState.Add:
            self.hide_button("c")
        elif self.window_state == WindowState.Select:
            self.hide_button("c")
            self.hide_button("a")
        elif self.window_state == WindowState.View:
            self.hide_button("u")
            self.hide_button("s")
            self.hide_button("c")

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
