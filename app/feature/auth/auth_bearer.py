from jose import jwt
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ...envConfig import Config


def decodeJWT(jwtoken: str):
    try:
        # decode and verify the token
        payload = jwt.decode(jwtoken, Config.JWT_SECRET_KEY, Config.ALGORITHM)
        return payload
    except Exception as e:
        print(e)
        raise e


def decodeRefreshJWT(refresh_jwtoken: str):
    try:
        # decode and verify the token
        payload = jwt.decode(
            refresh_jwtoken, Config.JWT_REFRESH_SECRET_KEY, Config.ALGORITHM
        )
        return payload
    except Exception as e:
        print(e)
        raise e


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme",
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization credentials",
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    def verify_refresh_jwt(self, refresh_jwtoken: str) -> bool:
        isTokenValid = False
        try:
            payload = decodeRefreshJWT(refresh_jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


jwt_bearer = JWTBearer()
