from interface.extra import Button
from interface.windows import MainMenu
from interface.window_types.window import Window
from logic.api import api
from utils.exceptions import NotFoundException


class ErrorMessage(Window):
    title  = "Error"
    def __init__(self, error_message):
        self.error_message = error_message
    
        
    def button_setup(self) -> None:
        self.buttons = [
        Button(letter="o", description="okay", function=self.back),
        ]

    def display(self) -> None:
        #a,b = self.exception_type
        self.boundary()
        self.centered("{}".format(self.error_message.__class__.__name__))
        self.centered("--------------------")
        self.centered("{}".format(str(self.error_message)))
        self.boundary()


    #def exception_type(self, exception_to_display):
     #   return type(exception_to_display), exception_to_display