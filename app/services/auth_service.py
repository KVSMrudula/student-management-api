
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.security import hash_password, verify_password


# User Registration
def register_user(db: Session, email: str, password: str):

    # Check whether user already exists
    existing_user = user_repository.get_user_by_email(
        db, email
    )

    if existing_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_password = hash_password(password)

    # Save user in database
    new_user = user_repository.create_user(
        db,
        email,
        hashed_password
    )

    return new_user


# User Login Authentication
def authenticate_user(db: Session, email: str, password: str):

    # Find user by email
    user = user_repository.get_user_by_email(db, email)

    # Check whether user exists
    if user is None:
        return None

    # Verify the entered password
    if not verify_password(password, user.hashed_password):
        return None

    # Check whether account is active
    if not user.is_active:
        return None

    return user
