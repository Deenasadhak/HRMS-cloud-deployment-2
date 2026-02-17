from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Float, Date
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HR = "hr"
    EMPLOYEE = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One-to-One relationship with Employee
    employee = relationship("Employee", back_populates="user", uselist=False)

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    designation = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    date_of_joining = Column(Date, nullable=False)
    salary = Column(Float, nullable=False) # Basic salary

    user = relationship("User", back_populates="employee")
    department = relationship("Department", back_populates="employees")
    attendance = relationship("Attendance", back_populates="employee")
    leaves = relationship("LeaveRequest", back_populates="employee")
    payroll = relationship("Payroll", back_populates="employee")
