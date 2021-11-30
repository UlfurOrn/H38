from interface.windows.window import Window


class OptionWindow(Window):
    options: list

    def run(self) -> None:
        while True:
            self.clear()
            self.display_options()
            data = self.get_input()
            self.parse_input(data)

    def display_options(self) -> None:
        self.boundary()
        self.title("Main Menu")
        self.boundary()
        self.empty()
        for index, option in enumerate(self.options, start=1):
            self.padded(f"{index}: {option}")
        self.empty()
        self.boundary()

    def parse_input(self, data: str) -> None:
        if not data.isdigit():
            raise Exception("Invalid Input: Input must be a valid integer")

        index = int(data) - 1
        if index not in range(len(self.options)):
            raise Exception("Invalid Input: Input must be a valid option")

        print(self.options[index])


class MainMenu(OptionWindow):
    options = ["Employees", "Locations", "Contractors", "Requests", "Reports"]
