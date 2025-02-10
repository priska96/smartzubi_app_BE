import os
import bcrypt
from datetime import datetime, timedelta, UTC
from typing import Union, Any
from jose import jwt
import smtplib
from email.mime.text import MIMEText

from ...envConfig import Config


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
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, Config.ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[Any], expires_delta: int = None) -> str:
    if expires_delta:
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        expires_delta = datetime.now(UTC) + timedelta(
            minutes=Config.REFRESH_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Config.JWT_REFRESH_SECRET_KEY, Config.ALGORITHM)

    return encoded_jwt


def send_email(to_email: str, subject: str, content: str):
    sender_email = ""
    sender_password = ""

    message = MIMEText(content)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
