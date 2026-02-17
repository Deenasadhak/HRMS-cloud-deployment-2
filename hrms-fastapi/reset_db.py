from app.database import Base, engine
from app.models.core import User, Department, Employee
from app.models.hr import Attendance, LeaveRequest, Payroll
import sys

print("Registered tables:", Base.metadata.tables.keys())

# Step 0: Clean slate
print("Dropping all tables...")
try:
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped.")
except Exception as e:
    print(f"Error dropping tables: {e}")

# Step 1: Users and Departments
print("Creating Users and Departments...")
try:
    Base.metadata.create_all(bind=engine, tables=[User.__table__, Department.__table__])
    print("Step 1 Success.")
except Exception as e:
    print(f"Step 1 Failed: {e}")
    sys.exit(1)

# Step 2: Employees (depends on Users/Departments)
print("Creating Employees...")
try:
    Base.metadata.create_all(bind=engine, tables=[Employee.__table__])
    print("Step 2 Success.")
except Exception as e:
    print(f"Step 2 Failed: {e}")
    sys.exit(1)

# Step 3: HR tables (depends on Employees)
import traceback

# ... (Step 3) ...
print("Creating HR tables...")
try:
    Base.metadata.create_all(bind=engine, tables=[Attendance.__table__, LeaveRequest.__table__, Payroll.__table__])
    print("Step 3 Success.")
except Exception as e:
    with open("db_error.log", "w") as f:
        f.write(f"Step 3 Failed: {e}\n")
        traceback.print_exc(file=f)
    print("Step 3 Failed. Check db_error.log")
    sys.exit(1)

print("All tables created successfully!")
