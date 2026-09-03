import logging

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User
from schemas.auth import LoginResponse
from schemas.users import UserCreate
from utils.jwt_helper import create_access_token

logger = logging.getLogger(__name__)


def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.scalar(select(User).where(User.email == user_data.email))

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    db.add(user)
    db.flush()

    logger.info(f"User with username `{user_data.email}` has been successfully created")

    return user


password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        password_hasher.verify(password_hash, password)
        return True
    except (InvalidHashError, VerificationError):
        return False


def login_user(email: str, password: str, db: Session):
    user = db.scalar(select(User).filter(User.email == email))
    if not user:
        logger.warning(f"User with `{email}` does not exist")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    is_valid_password = verify_password(
        password_hash=user.password_hash, password=password
    )
    if not is_valid_password:
        logger.warning(f"Incorrect password entered for user with `{email}`")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    logger.info(
        f"User with username `{email}` is successfully logged in "
        f"with user id `{user.id}`"
    )
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
    )
