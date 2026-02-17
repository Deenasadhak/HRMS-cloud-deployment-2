from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import employees, hr
from app.database import Base, engine

# Create tables matching models (until we use Alembic completely)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Backend")

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500", # Common Live Server port
    "http://127.0.0.1:3000", # Common frontend port
    "null", # Allow file:// requests if needed for local testing without a server
    "*" # For development simplicity, allow all. Reduce in production.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
import os

app.include_router(employees.router)
app.include_router(hr.router)

# Mount the frontend directory
# We assume the layout:
# root/
#   hrms-fastapi/app/main.py
#   hrms-frontend/

# Go up 3 levels from app/main.py to get to root
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(root_dir, "hrms-frontend")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    @app.get("/")
    def root():
        return {"message": "Frontend not found at " + frontend_path}
