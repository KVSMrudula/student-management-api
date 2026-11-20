
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.repositories import user_repository
from app.schemas import UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Get Current User Profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# Update Current User Profile
@router.put("/me", response_model=UserResponse)
def update_my_profile(
    user_data: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

    # Find the logged-in user
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check whether a new email was provided
    if user_data.email is not None:

        # Check whether email is already registered
        existing_user = user_repository.get_user_by_email(
            db, user_data.email
        )

        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Update email in database
        user = user_repository.update_user_email(
            db, user, user_data.email
        )

    return user


# Get User by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

    # Find the logged-in user
    current_user = user_repository.get_user_by_id(
        db, current_user_id
    )

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authenticated user not found"
        )

    # Allow users to view only their own profile.
    # Admins can view any user's profile.
    if current_user.role != "admin" and current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this user's profile"
        )

    # Find the requested user
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# Get All Users
@router.get("/", response_model=list[UserResponse])
def get_all_users(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

    users = user_repository.get_all_users(db)

    return users

# Delete Current User Account
@router.delete("/me")
def delete_my_account(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

    # Find the logged-in user
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete user from database
    user_repository.delete_user(db, user)

    return {
        "message": "Account deleted successfully"
    }
