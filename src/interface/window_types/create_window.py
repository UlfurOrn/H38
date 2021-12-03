from interface.extra import CreateField
from interface.window_types.window import Window


class CreateWindow(Window):
    info: dict
    fields: list[CreateField]
    current: int

    def window_setup(self) -> None:
        self.current = 0
        self.info = {}

    def setup(self) -> None:
        for field in self.fields:
            if field.required and self.info.get(field.field) is None:
                self.hide_button("s")  # Submit

        if not self.fields[self.current].submenu:
            self.hide_button("f")  # Open submenu

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
