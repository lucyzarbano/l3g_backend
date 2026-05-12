from fastapi import APIRouter, HTTPException, status

from lib.auth import authenticate_admin, create_access_token
from lib.config import settings
from models.schemas import LoginRequestSchema, TokenSchema

router = APIRouter()


@router.post("/login", response_model=TokenSchema)
def login(payload: LoginRequestSchema) -> TokenSchema:
    if not authenticate_admin(payload.username, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return TokenSchema(
        access_token=create_access_token(payload.username),
        token_type="bearer",
        expires_in=settings.jwt_expires_minutes * 60,
    )

