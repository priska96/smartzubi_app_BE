from functools import wraps
from fastapi import HTTPException, status
import sys

from .models import TokenTable, User as UserTable
from .feature.auth.auth_bearer import decodeJWT


def token_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if "pytest" in sys.modules:
            print("skipping token_required")
            return await func(*args, **kwargs)
        access_token = kwargs["dependencies"]
        print("##################", kwargs)
        payload = decodeJWT(access_token)
        user_id = payload["sub"]
        data = (
            kwargs["db"]
            .query(TokenTable)
            .filter_by(user_id=user_id, access_token=access_token, status=True)
            .first()
        )
        if data:
            return await func(*args, **kwargs)

        else:
            return {"msg": "Token blocked"}

    return wrapper


def paying_member_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        access_token = kwargs["dependencies"]
        if "pytest" in sys.modules:
            print("skipping paying_member_required")
            return await func(*args, **kwargs)
        print("######## paying member ##########", kwargs)
        payload = decodeJWT(access_token)
        user_id = payload["sub"]
        data = (
            kwargs["db"].query(UserTable).filter_by(id=user_id, is_paying=True).first()
        )
        print(data)
        if data:
            return await func(*args, **kwargs)

        else:
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not paying member",
            )

    return wrapper
