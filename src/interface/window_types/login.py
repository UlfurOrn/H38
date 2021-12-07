from interface.extra import Button
from interface.windows import MainMenu
from interface.window_types.window import Window
from logic.api import api
from utils.exceptions import NotFoundException

class Login(Window):
    title  = "Login"
    def __init__(self):
        self.ssn_dicty = [""]
        
    def button_setup(self) -> None:
        self.buttons = [
        Button(letter="b", description="back", function=self.back),
        Button(letter="press enter", description="login", function=self.parse_data)
        ]

    def display(self) -> None:
        self.boundary()
        self.centered("SSN:")
        for ssn in self.ssn_dicty:
            self.centered(ssn)
        self.boundary()

    def ssn_dict(self, data: str):
        if data in self.ssn_dicty:
            print("User already exists")
        else:
            self.ssn_dicty.append(data)
        return self.ssn_dicty

        
    #def __str__(self):
    #    s = ""
    #    s += "{}\n".format(x for x in self.ssn_dicty)
    #    return s


    def parse_input(self, data: str):
        """Call login with ssn, if error display error else go to main menu"""
        try:
            api.authentication.login(data)
            print()
            print("Succesfully logged in")
            MainMenu().run()
        except NotFoundException:
            print("User not found")
        
        

    def every_ssn(self):
        return (x for x in self.ssn_dicty)


