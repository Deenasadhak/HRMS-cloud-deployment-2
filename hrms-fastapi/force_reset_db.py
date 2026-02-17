from app.database import engine
from sqlalchemy import text
from sqlalchemy.schema import MetaData

# Reflect *all* tables from the DB
metadata = MetaData()
metadata.reflect(bind=engine)

print(f"Found tables: {list(metadata.tables.keys())}")

print("Dropping all reflected tables...")
metadata.drop_all(bind=engine)
print("All tables dropped.")

# Now run the original create logic
from app.database import Base
from app.models import core, hr
print("Creating new tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
