from typing import Any

from interface.extra import BACK, Button


class Window:
    WINDOW_SIZE = 50
    title: str
    buttons: list[Button]

    def run(self) -> Any:
        self.button_setup()
        self.window_setup()
        while True:
            self.setup()
            self.display_title()
            self.display()
            self.display_buttons()

            data = self.get_input()

            value = self.check_buttons(data)
            value = value or self.parse_input(data)

            if value:
                return value

            self.reset()
            self.clear()

    def button_setup(self) -> None:
        raise NotImplementedError()

    def window_setup(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def display(self) -> None:
        raise NotImplementedError()

    def display_title(self) -> None:
        self.boundary()
        self.centered(self.title)

    def display_buttons(self) -> None:
        self.padded()
        self.boundary()

    def hide_button(self, letter: str) -> None:
        for button in self.buttons:
            if button.letter == letter:
                button.hidden = True

    def check_buttons(self, data: str) -> Any:
        for button in self.buttons:
            if not button.hidden and button.letter == data:
                return button.function()

    def parse_input(self, data: str) -> Any:
        pass

    def reset(self) -> None:
        for button in self.buttons:
            button.hidden = False

    def _get_boundary(self) -> str:
        line = "-" * (self.WINDOW_SIZE - 2)
        return "+" + line + "+"

    def centered(self, text: str) -> None:
        print(f"|{text.center(self.WINDOW_SIZE - 2)}|")

    def padded(self) -> None:
        len_per_button = (self.WINDOW_SIZE - 2) / len(self.buttons)
        string = "|"

        for button in self.buttons:
            if not button.hidden:
                button_string = f"{button.letter}: {button.description}"
                formatted_butt_string = "{:^{}}".format(button_string, round(len_per_button))
                string += formatted_butt_string

        string += "|"
        print(string)

    def boundary(self) -> None:
        print(self._get_boundary())

    def empty(self) -> None:
        print("|" + " " * (self.WINDOW_SIZE - 2) + "|")

    def clear(self) -> None:
        print("\n" * 5)

    def get_input(self, text: str = "Enter Command: ") -> str:
        print()
        return input(text).strip()

    def back(self) -> BACK:
        return BACK
