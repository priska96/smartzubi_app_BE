import datetime
from pydantic import BaseModel


class UserCreateReq(BaseModel):
    username: str
    email: str
    password: str


class UserCreateRes(BaseModel):
    user_id: int


class LoginReq(BaseModel):
    email: str
    password: str
    userAgent: str


class LoginRes(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int


class LogoutRes(BaseModel):
    message: str


class ChangePasswordReq(BaseModel):
    email: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime


class TokenRefreshReq(BaseModel):
    refresh_token: str
    user_id: int


class TokenRefreshRes(BaseModel):
    access_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
