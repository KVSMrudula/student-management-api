
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):

    # Database table name
    __tablename__ = "users"

    # User ID
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # User email
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    # Hashed password
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # User role
    role: Mapped[str] = mapped_column(
        String(20),
        default="user"
    )

    # Account status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
