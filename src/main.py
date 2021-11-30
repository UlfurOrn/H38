from database.models.employee_model import Employee

if __name__ == "__main__":
    employees = Employee.all()

    employee = employees[0]

    print(employee)
