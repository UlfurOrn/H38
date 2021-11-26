# Endpoints:

### Employees:
* Get Employees
* Create Employee
* Get Employee
* Update Employee


### Locations:
* Get Locations
* Create Location
* Get Location
* Update Location


### Properties:
* Get Properties
* Create Property
* Get Property
* Update Property

### Facilities:
* Get Facilities for Property
* Create Facilities for Property
* Create Facility for Property
* Update Facility for Property


### Work Requests:
* Get Work Requests
* Create Work Request
* Get Work Request
* Update Work Request


### Work Reports:
* Get Work Reports
* Create Work Report
* Get Work Report
* Update Work Report
* Approve Work Report
* Disapprove Work Report
* Close Work Report


### Contractors:
* Get Contractors
* Create Contractor
* Get Contractor
* Update Contractor
* Grade Contractors





## Employees:

### Get Employees:
The method `get_all` should return all the employees in the system. This method
should be available for all users.

It should provide five parameters detailed here:
* `page` - The page parameter is required and is used for paginating the result.
* Filter parameters:
    * `filter_by` - This parameter should take in an Enum that tells us by what field we
    are filtering (Location).
    * `filter` - This parameter should take in the ID of the object we are filtering by.
    For example, in the case of finding all employees from a specific location, this
    parameter would hold the ID of said location.
* Search parameters:
    * `search_by` - This parameter should take in a string that tells us by what field we
    are searching (name, ssn, phone, etc...).
    * `search` - This parameter should take in the value we are actually searching by.

The system will additionally check for the following constraints:
* The `page` parameter is within 1 and max page (BadRequest)
* The `filter` parameter must be an existing ID (BadRequest)

This method should then return the following:
```
EmployeeList(
    page: int = 1,
    max_page: int = 3
    count: int = 25,
    items: list[EmployeeItem] = [
        EmployeeItem(
            employee_id: str = "1234567890abcdef"
            name: str = "Úlfur Örn Björnsson",
            security_number: int = 2811002110,
            work_phone: int = 6627880
        ),
        ...  
    ]
)
```


### Create Employee:
The method `create` should create an employee in the system. This method
should only be available to supervisors.

It should take in a single parameter that is the create employee model.
This input looks like the following:
```
CreateEmployeeInput(
    name: str = "Úlfur Örn Björnsson",
    security_number: int = 2811002110,
    address: str = "Heiðargerði 21",
    home_phone: int = 5812345,
    work_phone: int = 6627880,
    email: str = "ulfurinn@gmail.com",
    location_id: str = "123456789abcdef"
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* The social security number is unique (BadRequest)
* All required attributes are set (BadRequest)
* The location ID exists in the system (NotFound)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the created employee:
```
employee_id: str = "1234567890abcdef"
```


### Get Employee:
The method `get_single` should return a detailed model of an employee from the system.
This method should be available for all users.

It should take in a single parameter that is the ID of the employee.

The system will additionally check for the following constraints:
* The employee ID provided should exist in the system (NotFound)

This method should then return the following:
```
EmployeeInfo(
    employee_id: str = "1234567890abcdef"
    name: str = "Úlfur Örn Björnsson",
    security_number: int = 2811002110,
    address: str = "Heiðargerði 21",
    home_phone: int = 5812345,
    work_phone: int = 6627880,
    email: str = "ulfurinn@gmail.com",
    location_id: str = "123456789abcdef",
    location: str = "Keflavík, Airport"
)
```


### Update Employee:
The method `update` should update an employee in the system. This method
should only be available to supervisors.

It should take in a single parameter that is the update employee model.
This input looks like the following:
```
UpdateEmployeeInput(
    name: str = "Úlfur Örn Björnsson",
    address: str = "Heiðargerði 21",
    home_phone: int = 5812345,
    work_phone: int = 6627880,
    email: str = "ulfurinn@gmail.com",
    location_id: str = "123456789abcdef"
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* The location ID exists in the system (NotFound)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the employee changed:
```
employee_id: str = "1234567890abcdef"
```



## Locations:

### Get Locations:
The method `get_all` should return all the locations in the system.
This method should be available for all users.

It should provide five parameters detailed here:
* `page` - The page parameter is required and is used for paginating the result.
* Filter parameters:
    * `filter_by` - This parameter should take in an Enum that tells us by what field we
    are filtering (Country).
    * `filter` - This parameter should take in the value we are filtering by.
    For example, in the case of finding all locations from a specific country, this
    parameter would hold the name of said country.
* Search parameters:
    * `search_by` - This parameter should take in a string that tells us by what field we
    are searching (country, airport...).
    * `search` - This parameter should take in the value we are actually searching by.

The system will additionally check for the following constraints:
* The `page` parameter is within 1 and max page (BadRequest)
* The `filter` parameter must be an existing ID (BadRequest)

This method should then return the following:
```
LocationList(
    page: int = 1,
    max_page: int = 3
    count: int = 25,
    items: list[LocationItem] = [
        LocationItem(
            location_id: str = "1234567890abcdef",
            country: str = "Iceland",
            airport: str = "Keflavík, Airport"
        ),
        ...  
    ]
)
```


### Create Location:
The method `create` should create a location in the system.
This method should only be available to supervisors.

It should take in a single parameter that is the create location model.
This input looks like the following:
```
CreateLocationInput(
    country: str = "Iceland",
    airport: str = "Keflavík, Airport",
    phone: int = 5812345,
    opening_hours: str = "08:00-20:00",
    supervisor_id: str = "1234567890abcdef"
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* All required attributes are set (BadRequest)
* The supervisor (employee) ID exists in the system (NotFound)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the created location:
```
location_id: str = "1234567890abcdef"
```


### Get Location:
The method `get_single` should return a detailed model of a location from the system.
This method should be available for all users.

It should take in a single parameter that is the ID of the location.

The system will additionally check for the following constraints:
* The location ID provided should exist in the system (NotFound)

This method should then return the following:
```
LocationInfo(
    location_id: str = "1234567890abcdef"
    country: str = "Iceland",
    airport: str = "Keflavík, Airport",
    phone: int = 5812345,
    opening_hours: str = "08:00-20:00",
    supervisor_id: str = "1234567890abcdef",
    supervisor: str = "Úlfur Örn Björnsson"
)
```


### Update Location:
The method `update` should update a location in the system. This method
should only be available to supervisors.

It should take in a single parameter that is the update location model.
This input looks like the following:
```
UpdateLocationInput(
    airport: str = "Keflavík, Airport",
    phone: int = 5812345,
    opening_hours: str = "08:00-20:00",
    supervisor_id: str = "1234567890abcdef"
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* The location ID exists in the system (NotFound)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the employee changed:
```
employee_id: str = "1234567890abcdef"
```



## Properties:

### Get Properties:
The method `get_all` should return all the properties in the system.
This method should be available for all users.

It should provide five parameters detailed here:
* `page` - The page parameter is required and is used for paginating the result.
* Filter parameters:
    * `filter_by` - This parameter should take in an Enum that tells us by what field we
    are filtering (Location, Condition...).
    * `filter` - This parameter should take in the value we are filtering by.
    For example, in the case of finding all properties in a specific location, this
    parameter would hold the ID of said location.
* Search parameters:
    * `search_by` - This parameter should take in a string that tells us by what field we
    are searching (property number...).
    * `search` - This parameter should take in the value we are actually searching by.

The system will additionally check for the following constraints:
* The `page` parameter is within 1 and max page (BadRequest)
* The `filter` parameter must be an existing ID (BadRequest)

This method should then return the following:
```
PropertyList(
    page: int = 1,
    max_page: int = 3
    count: int = 25,
    items: list[PropertyItem] = [
        PropertyItem(
            property_id: str = "1234567890abcdef",
            property_number: str = "WTF is that???",
            location_id: str = "1234567890abcdef",
            condition: Condition = Condition.Good
        ),
        ...  
    ]
)
```


### Create Property:
The method `create` should create a property in the system.
This method should only be available to supervisors.

It should take in a single parameter that is the create property model.
This input looks like the following:
```
CreatePropertyInput(
    property_number: str = "WTF is that???",
    location_id: str = "1234567890abcdef",
    condition: Condition = Condition.Good
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* The property number is unique (BadRequest)
* All required attributes are set (BadRequest)
* The location ID exists in the system (NotFound)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the created property:
```
property_id: str = "1234567890abcdef"
```


### Get Property:
The method `get_single` should return a detailed model of a property from the system.
This method should be available for all users.

It should take in a single parameter that is the ID of the property.

The system will additionally check for the following constraints:
* The property ID provided should exist in the system (NotFound)

This method should then return the following:
```
PropertyInfo(
    property_id: str = "1234567890abcdef"
    property_number: str = "WTF is that???",
    location_id: str = "1234567890abcdef",
    location: str = "Keflavík, Airport",
    condition: Condition = Condition.Good,
    facility_count: int = 25
)
```


### Update Property:
The method `update` should update a property in the system. This method
should only be available to supervisors.

It should take in a single parameter that is the update property model.
This input looks like the following:
```
UpdatePropertyInput(
    location_id: str = "1234567890abcdef",
    condition: Condition = Condition.Good
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* The property ID exists in the system (NotFound)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the property changed:
```
property_id: str = "1234567890abcdef"
```


## Facilities:

### Get Facilities for Property:
The method `get_all_facilites` should return all the facilities for a property.
This method should be available for all users.

It should provide five parameters detailed here as well as the property ID:
* `page` - The page parameter is required and is used for paginating the result.
* Filter parameters:
    * `filter_by` - This parameter should take in an Enum that tells us by what field we
    are filtering (Condition...).
    * `filter` - This parameter should take in the value we are filtering by.
    For example, in the case of finding all facilities with a specific condition, this
    parameter would hold the value of said condition.
* Search parameters:
    * `search_by` - This parameter should take in a string that tells us by what field we
    are searching (name...).
    * `search` - This parameter should take in the value we are actually searching by.

The system will additionally check for the following constraints:
* The `page` parameter is within 1 and max page (BadRequest)
* The `filter` parameter must be an existing ID (BadRequest)

This method should then return the following:
```
FacilityList(
    page: int = 1,
    max_page: int = 3
    count: int = 25,
    items: list[FacilityItem] = [
        FacilityItem(
            facility_id: str = "1234567890abcdef",
            name: str = "WTF is that???",
            condition: Condition = Condition.Good
        ),
        ...  
    ]
)
```


### Create Facility for Property:
The method `create_facility` should create a facility for the property.
This method should only be available to supervisors.

It should take in a single parameter that is the create property model as well as the property ID.
This input looks like the following:
```
CreateFacilityInput(
    name: str = "Hot Tub",
    condition: Condition = Condition.Good
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* All required attributes are set (BadRequest)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the created facility:
```
facility_id: str = "1234567890abcdef"
```


### Get Property:
The method `get_single_facility` should return a detailed model of a facility from the system.
This method should be available for all users.

It should take in a single parameter that is the ID of the facility.

The system will additionally check for the following constraints:
* The facility ID provided should exist in the system (NotFound)

This method should then return the following:
```
FacilityInfo(
    facility_id: str = "1234567890abcdef"
    name: str = "Hot Tub",
    condition: Condition = Condition.Good
)
```


### Update Property:
The method `update_facility` should update a facility in the system. This method
should only be available to supervisors.

It should take in a single parameter that is the update property model as well as a facility ID.
This input looks like the following:
```
UpdateFacilityInput(
    name: str = "Hot Tub",
    condition: Condition = Condition.Good
)
```

The system will additionally check for the following constraints:
* The user must be a supervisor (Forbidden)
* The facility ID exists in the system (NotFound)
* Any other validation requirements we decide to implement (TBD)

Afterwards the system will respond with the ID of the facility changed:
```
facility_id: str = "1234567890abcdef"
```
