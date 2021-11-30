class Window:
    WINDOW_SIZE = 50

    def _get_boundary(self) -> str:
        line = "-" * (self.WINDOW_SIZE - 2)
        return "+" + line + "+"

    def centered(self, text: str) -> None:
        print(f"|{text.center(self.WINDOW_SIZE - 2)}|")

    def boundary(self) -> None:
        print(self._get_boundary())

    def title(self, title: str) -> None:
        self.centered(title)
