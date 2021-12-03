from typing import Any, Optional

from interface.extra import BACK, Button, Return


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
        # ToDo: Implement display buttons function
        for button in self.buttons:
            if not button.hidden:
                self.padded(f"{button.letter}: {button.description}", 20)
        self.boundary()

    def hide_button(self, letter: str) -> None:
        for button in self.buttons:
            if button.letter == letter:
                button.hidden = True

    def check_buttons(self, data: str) -> Optional[Return]:
        for button in self.buttons:
            if button.letter == "b" and data == "b":
                return Return(levels=1, data=None)
            if not button.hidden and button.letter == data:
                return button.function()

    def parse_input(self, data: str) -> Optional[Return]:
        pass

    def reset(self) -> None:
        for button in self.buttons:
            button.hidden = False

    def _get_boundary(self) -> str:
        line = "-" * (self.WINDOW_SIZE - 2)
        return "+" + line + "+"

    def centered(self, text: str) -> None:
        print(f"|{text.center(self.WINDOW_SIZE - 2)}|")

    def padded(self, text: str, padding: int = 10) -> None:
        string = "|"
        string += " " * padding
        string += text
        if len(string) > self.WINDOW_SIZE:
            string = string[0 : self.WINDOW_SIZE - 2]  # noqa: E203
        string += " " * (self.WINDOW_SIZE - len(string) - 1)
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
