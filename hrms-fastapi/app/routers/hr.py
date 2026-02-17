from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Attendance, LeaveRequest, Employee, Payroll
from app.schemas.hr import AttendanceCreate, AttendanceResponse, LeaveCreate, LeaveResponse

router = APIRouter(
    prefix="/hr",
    tags=["hr"]
)

# Attendance
@router.post("/attendance", response_model=AttendanceResponse)
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/attendance/{employee_id}", response_model=List[AttendanceResponse])
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.employee_id == employee_id).all()
    return attendance

# Leave Management
@router.post("/leaves", response_model=LeaveResponse)
def apply_leave(leave: LeaveCreate, employee_id: int, db: Session = Depends(get_db)):
    # In real app, employee_id would come from current_user
    db_leave = LeaveRequest(**leave.dict(), employee_id=employee_id)
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

@router.get("/leaves/{employee_id}", response_model=List[LeaveResponse])
def get_leaves(employee_id: int, db: Session = Depends(get_db)):
    leaves = db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all()
    return leaves

# Payroll (Basic Read Implementation)
@router.get("/payroll/{employee_id}")
def get_payroll(employee_id: int, db: Session = Depends(get_db)):
    payroll = db.query(Payroll).filter(Payroll.employee_id == employee_id).all()
    return payroll
