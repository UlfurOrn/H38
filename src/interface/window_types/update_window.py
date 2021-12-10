from uuid import UUID

from interface.extra import Button, Field
from interface.window_types.window import Window
from logic.helpers import InfoModel


class UpdateWindow(Window):
    info: dict
    fields: list[Field]
    current: int = 0

    def __init__(self, model_id: UUID):
        self.model_id = model_id

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="s", description="submit", function=self.submit, supervisor=True),
            Button(letter="f", description="fill", function=self.submenu),
            Button(letter="c", description="clear", function=self.clear),
            Button(letter="b", description="back", function=self.back),
        ]

    def window_setup(self) -> None:
        raise NotImplementedError()

    def setup(self) -> None:
        for field in self.fields:
            if field.required and self.info.get(field.field) is None:
                self.hide_button("s")  # Submit button

        if not self.fields[self.current].submenu:
            self.hide_button("f")  # Open submenu button

        while not self.fields[self.current].mutable:
            self.current = (self.current + 1) % len(self.fields)

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
            value = str(value)
            if field == self.fields[self.current]:
                value = value[:7] + " <---"

            string = f"|{field.name:>16}: "
            if value and len(value) > 28:
                txt_lst = value.split(" ")
                for i in txt_lst:
                    if len(string) < 48:
                        string += i + " "
                    else:
                        new_string = string[:-1]
                        new_string += "|"
                        print(new_string)
                        string = f"|{i:>16}"
                fin_string_len = len(string)
                string +=  " "*(49 - int(fin_string_len))
                string += "|"
                print(string)
            else:
                print(f"|{field.name:>16}: {value:<30}|")

    def parse_input(self, data: str) -> None:
        if data:
            field = self.fields[self.current]
            if not field.submenu:
                self.info[field.field] = data

        self.current = (self.current + 1) % len(self.fields)

    def submit(self) -> UUID:
        raise NotImplementedError()

    def submenu(self) -> InfoModel:
        raise NotImplementedError()

    def clear(self) -> None:
        field = self.fields[self.current]
        self.info[field.field] = None
