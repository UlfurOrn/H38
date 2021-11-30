import sys
import os
from uuid import UUID
from database.models.employee_model import Employee
from database.models.property_model import Property

print("Here:", os.path.relpath(__file__))


employee = Employee.get(UUID("e42cee48-1424-45a3-95a6-3d6037a57d5f"))


property = Property(
    property_number = "property1234",
    condition = "good",
    location_id = "cd314c5c-1cc3-4376-9003-6529b14cda8f"
).create()
