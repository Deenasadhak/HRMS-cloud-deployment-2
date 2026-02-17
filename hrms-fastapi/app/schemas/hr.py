from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LATE = "late"

class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: AttendanceStatus

class AttendanceResponse(AttendanceCreate):
    id: int
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None

    class Config:
        from_attributes = True

class LeaveType(str, Enum):
    SICK = "sick"
    CASUAL = "casual"
    EARNED = "earned"
    UNPAID = "unpaid"

class LeaveCreate(BaseModel):
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: Optional[str] = None

class LeaveResponse(LeaveCreate):
    id: int
    employee_id: int
    status: str
    applied_on: datetime

    class Config:
        from_attributes = True
