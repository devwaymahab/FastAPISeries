from fastapi import FastAPI, Body, HTTPException, status

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Hello FastAPI"
    }

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


@app.get("/employees")
def get_employees(page:int=1,limit:int=2):
    start_index = (page-1)*limit #1->0,2->(2-1)*2=1*2=2,3->(3-1)*2=4
    end_index = start_index+limit
    
    return employees[start_index:end_index]

# @app.get("/employees")
# def get_employees(department:str="ALL",min_salary:int=0):
#     results=[]
#     for emp in employees:
#         if (department=="ALL" or emp["department"]==department) and emp["salary"]>=min_salary:
#             results.append(emp)
#     return results

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    for eachemp in employees:
        if eachemp["id"] == employee_id:
            return eachemp
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"Employee {employee_id} not found"
    )
    
            
    

@app.post("/employees",status_code=status.HTTP_201_CREATED)
def create_employee(employee: dict = Body(...)):
    if any(emp["id"] == employee.get("id") for emp in employees):
         raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Employee ID already exists"
                )
       
    employees.append(employee)
    return {
        "message": "Employee created succesfully",
        "employee": employee
    }
    
@app.put("/employees/{employee_id}")
def update_employee(employee_id:int, employee: dict = Body(...)):
    for emp in employees:
        if emp["id"]==employee_id:
            emp.update(employee)
           
            return {
                "message": "Employee updated successfully",
                "employee": employee
            }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee {employee_id} not found"
    )

@app.patch("/employees/{employee_id}")  
def partial_update_employee(employee_id:int, employee: dict=Body(...)):
    for emp in employees:
            if emp["id"]==employee_id:
                emp.update(employee)
                
            return {
                "message": "Employee partially updated successfully",
                "employee": employee
            }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee {employee_id} not found"
    )
    
@app.delete("/employees/{employee_id}",status_code=status.HTTP_204_NO_CONTENT)  
def delete_employee(employee_id:int):
    for emp in employees:
        if emp["id"]==employee_id:
            employees.remove(emp)
            return 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Employee {employee_id} not found"
    )