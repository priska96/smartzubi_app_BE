from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db

from ..api_wrappers import token_required
from ..feature.user.schemas import UserResponse
from ..feature.auth.auth_bearer import jwt_bearer
from ..feature.auth.auth_api import Auth
from ..feature.auth.schemas import (
    TokenRefreshReq,
    UserCreateReq,
    UserCreateRes,
    LoginReq,
    LoginRes,
)

# Create an APIRouter instance
router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/register", response_model=UserCreateRes)
async def create_user(obj_in: UserCreateReq, db: Session = Depends(get_db)):
    return Auth.register(obj_in, db)


@router.post("/login", response_model=LoginRes)
async def login_user(obj_in: LoginReq, db: Session = Depends(get_db)):
    return Auth.login(obj_in, db)


@router.post("/logout")
@token_required
async def login_user(db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)):
    access_token = dependencies
    return Auth.logout(access_token, db)


@router.get("/auth-user", response_model=UserResponse)
@token_required
async def read_users_me(
    db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)
):
    access_token = dependencies
    return Auth.get_current_user(access_token, db)


@router.post("/refresh", status_code=200)
@token_required
async def get_refresh_token(
    token_refresh: TokenRefreshReq,
    db: Session = Depends(get_db),
    dependencies=Depends(jwt_bearer),
):
    return Auth.refresh_access_token_via_refresh_token(token_refresh, db)
