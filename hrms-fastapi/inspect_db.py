from app.database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
with open("inspect_output.txt", "w") as f:
    f.write(f"Tables: {inspector.get_table_names()}\n")

    if "employees" in inspector.get_table_names():
        f.write("\nColumns in 'employees':\n")
        for col in inspector.get_columns("employees"):
            f.write(f" - {col['name']} ({col['type']})\n")
    else:
        f.write("'employees' table not found!\n")
