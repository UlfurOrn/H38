class Window:
    WINDOW_SIZE = 50

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
            string = string[0 : self.WINDOW_SIZE - 2]
        string += " " * (self.WINDOW_SIZE - len(string) - 1)
        string += "|"
        print(string)

    def boundary(self) -> None:
        print(self._get_boundary())

    def empty(self) -> None:
        print("|" + " " * (self.WINDOW_SIZE - 2) + "|")

    def title(self, title: str) -> None:
        self.centered(title)

    def clear(self) -> None:
        print("\n" * 5)

    def get_input(self, text: str = "Enter Command: ") -> str:
        print()
        return input(text)
