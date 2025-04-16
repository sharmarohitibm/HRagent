from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
from typing import List

app = FastAPI()

CSV_FILE = "employees.csv"

class LeaveRequest(BaseModel):
    employee_id: str
    leave_type: str
    number_of_leaves: int

def read_employees_from_csv() -> List[dict]:
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_employees_to_csv(employees: List[dict]):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ["Employee Name", "Employee ID", "Annual Leave", "Sick Leave", "Childcare Leave"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for emp in employees:
            writer.writerow(emp)
            
@app.get("/leave-balance/{employee_id}")
def get_leave_balance(employee_id: str):
    employees = read_employees_from_csv()

    for emp in employees:
        if emp["Employee ID"] == employee_id:
            return {
                "Employee Name": emp["Employee Name"],
                "Employee ID": emp["Employee ID"],
                "Remaining Leave Entitlement": {
                    "Annual Leave": emp["Annual Leave"],
                    "Sick Leave": emp["Sick Leave"],
                    "Childcare Leave": emp["Childcare Leave"]
                }
            }

    raise HTTPException(status_code=404, detail="Employee not found")

@app.post("/deduct-leave")
def deduct_leave(request: LeaveRequest):
    employees = read_employees_from_csv()
    updated = False

    for emp in employees:
        if emp["Employee ID"] == request.employee_id:
            leave_key = request.leave_type
            if leave_key not in ["Annual Leave", "Sick Leave", "Childcare Leave"]:
                raise HTTPException(status_code=400, detail="Invalid leave type")

            current_leave = int(emp[leave_key])
            if current_leave < request.number_of_leaves:
                raise HTTPException(status_code=400, detail="Not enough leave balance")

            emp[leave_key] = str(current_leave - request.number_of_leaves)
            updated = True
            write_employees_to_csv(employees)
            return emp

    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")


# Assuming CSV format like this
# Employee Name,Employee ID,Annual Leave,Sick Leave,Childcare Leave
# Alice Kim,EMP1023,25,10,6
# Jamal Turner,EMP1147,20,12,5
# Priya Desai,EMP1098,30,8,7
# Lucas Nguyen,EMP1210,18,15,4
# Sarah O'Malley,EMP1175,22,10,6


# Exmaple request POST
# {
#   "employee_id": "EMP1023",
#   "leave_type": "Sick Leave",
#   "number_of_leaves": 2
# }


# Example Response
# {
#   "Employee Name": "Alice Kim",
#   "Employee ID": "EMP1023",
#   "Annual Leave": "25",
#   "Sick Leave": "8",
#   "Childcare Leave": "6"
# }


