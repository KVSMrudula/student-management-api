
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# 1. Database URL
DATABASE_URL = "sqlite:///./login.db"


# 2. Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# 3. Create database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 4. Create Base class
class Base(DeclarativeBase):
    pass


# 5. Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
