from typing import Callable

from pydantic import BaseModel


class Button(BaseModel):
    letter: str
    description: str
    function: Callable


class Window:
    WINDOW_SIZE = 50
    title: str
    buttons: list[Button]

    def run(self):
        self.window_setup()
        while True:
            self.setup()
            self.display_title()
            self.display()
            self.display_buttons()

            data = self.get_input()

            if data == "b":
                return

            self.check_buttons(data)
            self.parse_input(data)

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
        print("|                                        b: back |")
        self.boundary()

    def check_buttons(self, data: str) -> None:
        for button in self.buttons:
            if button.letter == data:
                return button.function()

    def parse_input(self, data: str) -> None:
        pass

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
