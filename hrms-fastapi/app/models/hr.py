from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Enum, Float
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LATE = "late"

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in = Column(DateTime, nullable=True)
    check_out = Column(DateTime, nullable=True)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.ABSENT)

    employee = relationship("Employee", back_populates="attendance")

class LeaveStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveType(str, enum.Enum):
    SICK = "sick"
    CASUAL = "casual"
    EARNED = "earned"
    UNPAID = "unpaid"

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type = Column(Enum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    applied_on = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="leaves")

class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    month = Column(String, nullable=False) # e.g., "2023-10"
    basic_salary = Column(Float, nullable=False)
    additions = Column(Float, default=0.0) # Bonus, Allowances
    deductions = Column(Float, default=0.0) # Tax, PF
    net_salary = Column(Float, nullable=False)
    generated_on = Column(DateTime, default=datetime.utcnow)
    is_paid = Column(Integer, default=0) # 0=Unpaid, 1=Paid

    employee = relationship("Employee", back_populates="payroll")
