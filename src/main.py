import sys
import os
from uuid import UUID
from database.models.employee_model import Employee
from database.models.property_model import Property


#print("Here:", os.path.relpath(__file__))


#employee = Employee.get(UUID("e42cee48-1424-45a3-95a6-3d6037a57d5f"))


#property = Property(
#    property_number = "property1234",
#    condition = "good",
#    location_id = "cd314c5c-1cc3-4376-9003-6529b14cda8f"
#).create()

class Menu:
    def __init__(self):
        self.mainmenu = """
        +------------------------------------------------+
        |                    Main Menu                   |
        +------------------------------------------------+
        |                                                |
        |                1. Employees                    |
        |                2. Locations                    |
        |                3. Properties                   |
        |                4. Contractors                  |
        |                5. Work Requests                |
        |                6. Work Reports                 |
        |                                                |
        +------------------------------------------------+
        """
        self.employee_menu = """
        +------------------------------------------------+
        |                  Employees                     |
        +---+---------------------+------------+---------+
        | # |        Name         |    SSN     |  Phone  |
        +---+---------------------+------------+---------+
        | 0 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 1 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 2 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 3 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 4 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 5 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 6 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 7 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 8 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        | 9 | Úlfur Örn Björnsson | 2811002110 | 6627880 |
        +---+---------------------+------------+---------+
        | a: prev    page: 1/13     total: 128   d: next |
        +------------------------------------------------+
        | c: create    s: search    f: filter    b: back |
        +------------------------------------------------+
        """
        self.create_emplpoyee = """
        +------------------------------------------------+
        |                 Create Employee                |
        +------------------------------------------------+
        |                                                |
        |             Name:       <---                   |
        |              SSN:                              |
        |          Address:                              |
        |            Email:                              |
        |       Home Phone:                              |
        |       Work Phone:                              |
        |         Location:                              |
        |                                                |
        +------------------------------------------------+
        | s: submit      a: up      d: down      b: back |
        +------------------------------------------------+
        """
        
        self.location_menu = """
        +------------------------------------------------+
        |                   Locations                    |
        +---+---------------+----------------------------+
        | # |    Country    |           Airport          |
        +---+---------------+----------------------------+
        | 0 | Iceland       | Keflavík, Airport          |
        | 1 | Iceland       | Reykjavík, Airport         |
        | 2 | United States | United States, Airport     |
        | 3 | Britain       | Britain, Airport           |
        | 4 | France        | France, Airport            |
        | 5 | Italy         | Italy, Airport             |
        | 6 |               |                            |
        | 7 |               |                            |
        | 8 |               |                            |
        | 9 |               |                            |
        +---+---------------+----------------------------+
        | a: prev    page: 2/2     total: 16     d: next |
        +------------------------------------------------+
        | c: create    s: sort      f: filter    b: back |
        +------------------------------------------------+
        """

        self.create_location = """
        +------------------------------------------------+
        |                 Create Location                |
        +------------------------------------------------+
        |                                                |
        |          Country:       <---                   |
        |          Airport:                              |
        |            Phone:                              |
        |    Opening Hours:                              |
        |       Supervisor:                              |
        |                                                |
        +------------------------------------------------+
        | s: submit      a: up      d: down      b: back |
        +------------------------------------------------+
        """
        self.contractor_menu = """
        +------------------------------------------------+
        |                    Contractors                 |
        +---+---------------------+------------+---------+
        | # |        Name         |  Location  |  Phone  |
        +---+---------------------+------------+---------+
        | 0 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 1 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 2 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 3 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 0 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 1 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 2 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 3 |  Kristófer Andersen |   Iceland  | 6187515 |
        | 9 |  Kristófer Andersen |   Iceland  | 6187515 |
        +---+---------------------+------------+---------+
        | a: prev    page: 1/13     total: 128   d: next |
        +------------------------------------------------+
        | c: create    s: sort      f: filter    b: back |
        +------------------------------------------------+
        """
        self.create_contractor = """
        +------------------------------------------------+
        |                Create Contractor               |
        +------------------------------------------------+
        |                                                |
        |             Name:       <---                   |
        |    Contract Name:                              |
        |            Phone:                              |
        |    Opening Hours:                              |
        |         Location:                              |
        |       Work Phone:                              |
        |                                                |
        |                                                |
        +------------------------------------------------+
        | s: submit      a: up      d: down      b: back |
        +------------------------------------------------+
        """

        self.property_menu = """
        +------------------------------------------------+
        |                   Properties                   |
        +---+---------------+----------------------------+
        | # |    Location    |           Airport          |
        +---+---------------+----------------------------+
        | 0 | Iceland       | Keflavík, Airport          |
        | 1 | Iceland       | Reykjavík, Airport         |
        | 2 | United States | United States, Airport     |
        | 3 | Britain       | Britain, Airport           |
        | 4 | France        | France, Airport            |
        | 5 | Italy         | Italy, Airport             |
        | 6 |               |                            |
        | 7 |               |                            |
        | 8 |               |                            |
        | 9 |               |                            |
        +---+---------------+----------------------------+
        | a: prev    page: 2/2     total: 16     d: next |
        +------------------------------------------------+
        | c: create    s: sort      f: filter    b: back |
        +------------------------------------------------+
        """

        self.property_create = """
        +------------------------------------------------+
        |                 Create Property                |
        +------------------------------------------------+
        |                                                |
        |         Location:       <---                   |
        |        Condition:                              |
        |       Facilities:                              |
        |                                                |
        +------------------------------------------------+
        | s: submit      a: up      d: down      b: back |
        +------------------------------------------------+
        """

    def menu(self):
        print(self.mainmenu)
        self.get_input()
    

    def get_input(self):
        while True:
            user_input = input("Select option: ")
            if user_input == "1":
                Menu.employee(self)
            elif user_input == "2":
                Menu.locations(self)
            elif user_input == "3":
                Menu.property(self)
            elif user_input == "4":
                Menu.contractor(self)
            elif user_input == "5":
                pass
            elif user_input == "6":
                pass



    def employee(self):
        print(self.employee_menu)
        new_input = input("Select option: ")
        if new_input == "b":
            Menu.menu(self)
        elif new_input == "c":
            print(self.create_emplpoyee)


    def locations(self):
        print(self.location_menu)
        new_input = input("Select option: ")
        if new_input == "b":
            Menu.menu(self)
        elif new_input == "c":
            Menu.locations_opt_c(self)
        else:
            Menu.menu(self)
            

    def contractor(self):
        print(self.contractor_menu)
        new_input = input("Select option: ")
        if new_input == "b":
            Menu.menu(self)
        elif new_input == "c":
            print(self.create_contractor)

    def property(self):
        print(self.property_menu)
        new_input = input("Select option: ")
        if new_input == "b":
            Menu.menu(self)
        elif new_input == "c":
            Menu.contractor_opt_c(self)
            


    def locations_opt_c(self):
        print(self.create_location)

    def contractor_opt_c(self):
        new_input = input("")
        print(self.property_create)

if __name__ == "__main__":
    main_menu = Menu()
    main_menu.menu()


