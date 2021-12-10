import logging
from typing import Any

from pydantic import ValidationError

from interface.extra import BACK, Button
from logic.api import api
from utils.exceptions import BadRequestException, ForbiddenException, NotFoundException

logger = logging.getLogger(__name__)
logger.propagate = False  # This is done to prevent outputting to stdout
logger.setLevel(logging.WARNING)

log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("logfile.log")
file_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)


class Window:
    WINDOW_SIZE = 50
    title: str
    buttons: list[Button]

    def run(self) -> Any:
        self.button_setup()
        self.window_setup()
        while True:
            with ExceptionHandler():
                self.setup()
                self.display_title()
                self.display()
                self.display_buttons()

                data = self.get_input()
                value = self.parse_data(data)

                if value:
                    return value

            self.reset()
            self.clear_screen()

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
        user_is_supervisor = api.authentication.is_supervisor()

        buttons = [
            button
            for button in self.buttons
            if not (button.supervisor and not user_is_supervisor) and not button.hidden
        ]

        length_per_button = (self.WINDOW_SIZE - 2) / len(buttons)
        string = "|"

        for button in buttons:
            button_string = f"{button.letter}: {button.description}"
            string += "{:^{}}".format(button_string, round(length_per_button))

        string += "|"
        print(string)

        self.boundary()

    def hide_button(self, string: str) -> None:
        for button in self.buttons:
            if button.letter == string or button.description == string:
                button.hidden = True

    def parse_data(self, data: str) -> Any:
        user_is_supervisor = api.authentication.is_supervisor()
        for button in self.buttons:
            if button.supervisor and not user_is_supervisor:
                continue

            if not button.hidden and button.letter == data:
                return button.function()

        return self.parse_input(data)

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

    def clear_screen(self) -> None:
        print("\n" * 5)

    def get_input(self, text: str = "Enter Command: ") -> str:
        print()
        return input(text).strip()

    def back(self) -> BACK:
        return BACK


class ExceptionHandler:
    def to_title_case(self, snake_case: str) -> str:
        return snake_case.replace("_", " ").title()

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None:
            return True

        elif exception_type == ValidationError:
            errors = exception_value.errors()
            error_string = ""
            for error in errors:
                field = self.to_title_case(error["loc"][0])
                error_string += f"{field}:\n"
                error_string += error["msg"]
                error_string += "\n\n"

            window = ErrorWindow("Validation Error", error_string.strip())
            logger.exception(exception_value)

        elif exception_type == NotImplementedError:
            window = ErrorWindow(
                "Not Implemented", "This feature has not yet been completed,\ncoming soon in a release near you!"
            )

        # We do not want to catch all exceptions (KeyboardInterrupt for example) only subclasses of Exception
        elif not (exception_type == Exception or exception_type in Exception.__subclasses__()):
            return False

        elif exception_type in (BadRequestException, NotFoundException, ForbiddenException):
            window = ErrorWindow(exception_type.__name__, str(exception_value))
            logger.exception(exception_value)

        else:
            window = ErrorWindow("Internal Server Error", "Contact a System Admin for Support")
            logger.critical(exception_value)

        window.run()

        return True


class ErrorWindow(Window):
    title = "Error"

    def __init__(self, error_type, error_message):
        self.error_type = error_type
        self.error_message = error_message

    def button_setup(self) -> None:
        self.buttons = [Button(letter="o", description="okay", function=self.back)]

    def display(self) -> None:
        self.boundary()
        self.empty()

        self.centered(self.error_type)
        self.empty()
        for line in self.error_message.split("\n"):
            self.centered(line)

        self.empty()
        self.boundary()
