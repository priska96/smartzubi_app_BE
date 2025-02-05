import os
import bcrypt
from datetime import datetime, timedelta, UTC
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365  # 365 days
REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365 *1.5  # 1.5 years
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


# Hash a password using bcrypt
def get_hashed_password(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


def create_access_token(subject: Union[Any], expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        expires_delta = datetime.now(UTC) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[Any], expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        expires_delta = datetime.now(UTC) + timedelta(
            minutes=REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)

    return encoded_jwt
