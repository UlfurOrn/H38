from interface.extra import Button
from interface.windows import MainMenu
from interface.window_types.window import Window


class TestWindow(Window):
    title  = "Add user"
    def __init__(self):
        self.ssn_dicty = ["0107002210"]
        
    def button_setup(self) -> None:
        self.buttons = [
        Button(letter="b", description="back", function=self.back),
        Button(letter="", description="press enter", function=self.back),
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

        
    def __str__(self):
        s = ""
        s += "{}\n".format(x for x in self.ssn_dicty)
        return s


    def parse_input(self, data: str):
        # Add user to system
        valid_ssn = self.ssn_dicty  # Get SSN's
        if data in valid_ssn:
            print("User already exists")
        else:
            self.ssn_dict(data)
            print("User added")

    def every_ssn(self):
        return (x for x in self.ssn_dicty)


if __name__ == "__main__":
    # MainMenu().run()
    TestWindow().run()
