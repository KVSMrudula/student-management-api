
from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import auth, user

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Student Management API",
    description="Student Management and Authentication System",
    version="1.0.0"
)

# Register routers
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management API"
    }
