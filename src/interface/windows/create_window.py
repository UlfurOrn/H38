from interface.windows.window import Window


class CreateWindow(Window):
    info: str

    def display(self) -> None:
        self.boundary()
        self.empty()
        self.display_info()
        self.empty()
        self.boundary()

    def display_info(self) -> None:
        self.centered(self.info)


class EmployeeCreateWindow(CreateWindow):
    title = "Create Employee"
    info = "Employee Info"
    buttons = []
