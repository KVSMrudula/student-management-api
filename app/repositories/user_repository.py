
from sqlalchemy.orm import Session

from app.models import User


# Find user using email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Find user using ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()


# Create a new user
def create_user(
    db: Session,
    email: str,
    hashed_password: str
):
    new_user = User(
        email=email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def update_user_email(db: Session, user: User, new_email: str):

    user.email = new_email

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user: User):

    db.delete(user)

    db.commit()

    return True
