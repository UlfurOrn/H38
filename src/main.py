from interface.extra import Button
from interface.window_types.error_window import ErrorMessage
from interface.window_types.login import Login
from interface.windows import MainMenu
from interface.window_types.window import Window
from logic.api import api
from utils.exceptions import NotFoundException




if __name__ == "__main__":
    #MainMenu().run()
    Login().run()
