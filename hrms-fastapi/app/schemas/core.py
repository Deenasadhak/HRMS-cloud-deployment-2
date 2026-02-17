from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str = "employee"

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool

    class Config:
        from_attributes = True

# Employee Schemas
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    designation: Optional[str] = None
    department_id: Optional[int] = None
    date_of_joining: date
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
