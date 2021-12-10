from interface.extra import Button, Field
from interface.window_types.window import Window
from logic.helpers import FilterOptions, InfoModel


class FilterWindow(Window):
    info: dict
    fields: list[Field]
    current: int = 0

    def __init__(self, filter_options: FilterOptions):
        self.info = filter_options.dict()

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="s", description="save", function=self.save),
            Button(letter="f", description="fill", function=self.submenu),
            Button(letter="c", description="clear", function=self.clear),
            Button(letter="b", description="back", function=self.back),
        ]

    def setup(self) -> None:
        if not self.fields[self.current].submenu:
            self.hide_button("f")  # Hide open submenu button

    def display(self) -> None:
        self.boundary()
        self.empty()
        self.display_info()
        self.empty()
        self.boundary()

    def display_info(self) -> None:
        for field in self.fields:
            prefix = "+ " if field.submenu else ""
            value = self.info.get(field.field)
            value = value or ""
            value = str(value)
            if field == self.fields[self.current]:
                value = value[:7] + " <---"
            print(f"|{prefix + field.name:>16}: {value:<30}|")

    def parse_input(self, data: str) -> None:
        if data:
            field = self.fields[self.current]
            if not field.submenu:
                self.info[field.field] = data

        self.current = (self.current + 1) % len(self.fields)

    def save(self) -> FilterOptions:
        raise NotImplementedError()

    def submenu(self) -> None:
        raise NotImplementedError()

    def clear(self) -> None:
        field = self.fields[self.current]
        self.info[field.field] = None
