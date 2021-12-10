from uuid import UUID, uuid4
from datetime import date, datetime
from interface.extra import Button
from interface.window_types.login import Login
from interface.windows import MainMenu
from interface.window_types.window import Window
from logic.api import api
from logic.helpers import ListItem
from utils.exceptions import NotFoundException
from logic.logic.report_logic import ReportInfo


class ReportOverview(Window):
    reports = [
        ReportInfo(
            report_id=uuid4(),
            property_id=uuid4(),
            employee_id=uuid4(),
            description="Description",
            cost=500,
            status="Done",
            date=datetime.now().date(),
            contractor_id=uuid4() 
        ),
        ReportInfo(
            report_id=uuid4(),
            property_id=uuid4(),
            employee_id=uuid4(),
            description="Description 2",
            cost=5000,
            status="Done",
            date=datetime.now().date(),
            contractor_id=uuid4() 
        ),
    ]

    title  = "Report Overview"

    def button_setup(self) -> None:
        self.buttons = [
        Button(letter="a", description="next", function=self.back),
        Button(letter="b", description="back", function=self.parse_data),
        Button(letter="c", description="prev", function=self.back),
        ]

    def display(self) -> None:
        self.boundary()
        self.centered("S")
        self.boundary()


if __name__ == "__main__":
    #MainMenu().run()
    ReportOverview().run()
