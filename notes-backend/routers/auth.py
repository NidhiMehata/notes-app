from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import services.user as user_service
from database.database import get_db
from schemas.auth import LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> LoginResponse:
    from config import settings

    print("CORS origins:", settings.cors_origins)
    print("Parsed origins:", settings.cors_origins.split(","))
    return user_service.login_user(
        email=form_data.username, password=form_data.password, db=db
    )
