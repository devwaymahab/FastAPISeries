from fastapi import FastAPI, Body, HTTPException, status, Path

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

# PATH PARAMETERS
# Path parameters are values passed directly inside the URL path. They are commonly used to identify resources, such as retrieving an employee by ID, finding an employee by name, or accessing employees within a department.
# GET /employees/101
# GET /employees/102
# GET /departments/IT

@app.get("/employees/{employee_id}")
def get_employees(employee_id:int):
    for employee in employees:
        if employee["id"] == employee_id:
            return {"employee":employee,"employee_id_type":type(employee_id).__name__}
    raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found"
        )

@app.get("/employees/earning-above/{salary}")
def get_employees_by_salary(salary: float):
    results = []
    for emp in employees:
        if emp["salary"]>salary:
            results.append(emp)
            
    return results

@app.get("/departments/{department}/employees/{employee_id}")
def get_employees_by_department(department:str,employee_id:int):
    for employee in employees:
        if employee["department"]==department and employee["id"] == employee_id:
            return {"employee":employee,"employee_id_type":type(employee_id).__name__}
    raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found"
        )
    

@app.get("/employees/{employee_id}/name/{employee_name}")
def get_employees_by_name(employee_id:int,employee_name:str):
    for employee in employees:
        if employee["name"]==employee_name and employee["id"] == employee_id:
            return {"employee":employee,"employee_id_type":type(employee_id).__name__}
    raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found"
        )
    
    
#Path Parameter Constraints

@app.get("/employees/restricted/{employee_id}")
def get_restricted_employee(employee_id:int=Path(
    ge=101,
    le=110,
    description="Employee ID must be between 101 and 110"
)):
    for employee in employees:
        if employee["id"] == employee_id:
            return {"employee":employee,"employee_id_type":type(employee_id).__name__}
    raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Employee {employee_id} not found"
        )
    
# Common constraints
# Constraint	Meaning	Example
# gt=0	    Greater than zero	ID greater than 0
# ge=101	Greater than or equal to 101	ID starts at 101
# lt=111	Less than 111	ID below 111
# le=110	Less than or equal to 110	ID ends at 110


@app.get("/employees/by-name/{employee_name}")
def get_employee_by_name(employee_name:str=Path(
    min_length=3,
    max_length=15,
    description="Employee name must contain 3 to 15 characters")):
    for employee in employees:
        if employee["name"].lower() == employee_name.lower():
            return employee

    raise HTTPException(
        status_code=404,
        detail="Employee not found"
    )