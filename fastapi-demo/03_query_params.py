from fastapi import FastAPI, Body, HTTPException, status, Path, Query

app = FastAPI()


employees = [
    {"id": 101, "name": "Ravi", "department": "IT", "salary": 60000},
    {"id": 102, "name": "Sita", "department": "HR", "salary": 50000},
    {"id": 103, "name": "Kiran", "department": "IT", "salary": 70000},
    {"id": 104, "name": "Priya", "department": "Finance", "salary": 55000},
    {"id": 105, "name": "Arjun", "department": "IT", "salary": 65000},
    {"id": 106, "name": "Lakshmi", "department": "HR", "salary": 48000},
    {"id": 107, "name": "Rahul", "department": "Finance", "salary": 75000},
    {"id": 108, "name": "Anjali", "department": "IT", "salary": 58000},
    {"id": 109, "name": "Vijay", "department": "Sales", "salary": 52000},
    {"id": 110, "name": "Meena", "department": "Sales", "salary": 62000}
]

# Query parameters are values passed through a URL after the ? symbol. They are commonly used to filter, search, sort, and paginate data.

# /employees?department=IT
# /employees?department=HR
# /employees?min_salary=60000

# department=IT filters employees belonging to the IT department.
# department=HR filters employees belonging to the HR department.
# min_salary=60000 filters employees based on salary.

# /path?parameter1=value1&parameter2=value2&parameter3=value3


@app.get("/employees")
def get_employees(department:str):
    results = []
    for emp in employees:
        if emp["department"]==department:
            results.append(emp)
    return results

# Optional Query Parameters
@app.get("/employees/all")
def get_employees(department: str|None=None):

    if department is None:
        return employees

    result = []

    for employee in employees:
        if employee["department"].lower() == department.lower():
            result.append(employee)

    return result

# Default Values
@app.get("/employees/by-salary")
def get_employees_by_salary(min_salary:int=50000):
    results = []
    for emp in employees:
        if emp["salary"]>=min_salary:
            results.append(emp)
    return results

# Declaration	                 Required?	              Behavior
# department: str	                Yes	           Client must provide a department
# department: str = "IT"	        No	           Defaults to IT
# department: str | None = None 	No	           Defaults to None
# min_salary: int = 60000	        No	           Defaults to ₹60,000


#Query Parameter Type Validation
@app.get("/employees/min-salary")
def get_employees_by_min_salary(min_salary: int):

    result = []

    for employee in employees:
        if employee["salary"] >= min_salary:
            result.append(employee)

    return result

# Multiple Query Parameters
@app.get("/employees/search")
def search_employees(department:str|None=None,
                     min_salary:int=0,
                     max_salary:int=100000):
    results = []
    for emp in employees:
        if department is not None:
            if emp["department"]!=department:
                continue
        if emp["salary"]<min_salary:
            continue
        if emp["salary"]>max_salary:
            continue
        results.append(emp)
    return results

# Query Parameter Constraints
@app.get("/employees/validated-salary")
def get_employees_by_salary(min_salary:int=Query(
    ge=0,
    le=100000,
    description="Minimum salary must be between 0 and 100000"
)):
    results = []
    for emp in employees:
        if emp["salary"]>=min_salary:
            results.append(emp)
            
    return results


@app.get("/employees/search-by-name")
def search_employee_by_name(
    name: str = Query(
        min_length=3,
        max_length=15,
        description="Employee name must contain 3 to 15 characters"
    )
):

    result = []

    for employee in employees:
        if name.lower() in employee["name"].lower():
            result.append(employee)

    return result


# Common constraints
#-------------------------
# Constraint	     Meaning
# gt=0	        Greater than zero
# ge=0	        Greater than or equal to zero
# lt=100	        Less than 100
# le=100	        Less than or equal to 100
# min_length=3	At least three characters
# max_length=15	At most 15 characters
# pattern="..."	Must match a regular expression



@app.get("/employees/filter-salary")
def filter_salary(min_salary:int=Query(
    default=50000,
    ge=0,
    le=100000,
    title="Minimum Salary",
    description="Return employees earning at least this amount"
)):
    results = []
    for emp in employees:
        if emp["salary"]>=min_salary:
            results.append(emp)
            
    return results

#List query parameters
@app.get("/employees/by-departments")
def get_employees_by_department(departments: list[str]=Query(
    default=None,
    min_length=1,
    description="department name"
)):

    result = []
    
    for employee in employees:
        if employee["department"].lower() in [each.lower() for each in departments]:
            result.append(employee)

    return result



# Query parameters: Values passed after ? in a URL.
# Optional query parameters: Use a default value such as None.
# Default values: Used when the client omits a parameter.
# Type validation: FastAPI checks values against type annotations.
# Multiple query parameters: Combine filters in one URL using &.
# Query constraints: Use ge, le, min_length, max_length, and other supported options.
# Query(): Adds validation rules and metadata, and supports list-valued query parameters.