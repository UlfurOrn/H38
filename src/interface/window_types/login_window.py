from interface.extra import Button
from interface.window_types.window import Window
from interface.windows import MainMenu
from logic.api import api


class Login(Window):
    title = "Login"

    def button_setup(self) -> None:
        self.buttons = [Button(letter="b", description="back", function=self.back)]

    def display(self) -> None:
        self.boundary()
        self.empty()
        self.centered("Please enter your SSN:")
        self.empty()
        self.boundary()

    def parse_input(self, data: str):
        api.authentication.login(data)
        MainMenu().run()
