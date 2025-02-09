from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
import json

from ..user.schemas import UserResponse, UserExamRes
from .utils import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)
from .auth_bearer import decodeJWT, decodeRefreshJWT, jwt_bearer
from .auth_error_enum import AuthErrorEnum
from .schemas import (
    LoginReq,
    LoginRes,
    LogoutRes,
    TokenData,
    TokenRefreshReq,
    TokenRefreshRes,
    UserCreateReq,
    UserCreateRes,
)
from ... import models
import datetime


class Auth:
    def register(user: UserCreateReq, db: Session):
        existing_user = db.query(models.User).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthErrorEnum.email_exists,
            )

        encrypted_password = get_hashed_password(user.password)
        user.password = encrypted_password
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserCreateRes(user_id=db_user.id)

    def login(user_in: LoginReq, db: Session):
        db_user = (
            db.query(models.User).filter(models.User.email == user_in.email).first()
        )
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthErrorEnum.wrong_email,
            )
        hashed_pass = db_user.password
        if not verify_password(user_in.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthErrorEnum.wrong_password,
            )
        if db_user.locked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthErrorEnum.account_locked,
            )
        existing_token = (
            db.query(models.TokenTable)
            .filter(
                models.TokenTable.user_id == db_user.id,
                models.TokenTable.status == True,
            )
            .first()
        )
        if existing_token and db_user.email != "priska2@test.de":  # active session
            db_user.login_attempts += 1
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            print("login attempts", db_user.login_attempts)
            if db_user.login_attempts > 3:
                db_user.locked = True
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=AuthErrorEnum.account_too_many_attempts,
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthErrorEnum.account_has_sessoin,
            )

        access = create_access_token(db_user.id)
        refresh = create_refresh_token(db_user.id)

        token_db = models.TokenTable(
            user_id=db_user.id, access_token=access, refresh_token=refresh, status=True
        )
        db.add(token_db)
        db.commit()
        db.refresh(token_db)

        user_exams = [
            UserExamRes(
                id=x.id,
                exam_id=x.exam_id,
                created_at=x.created_at,
                title=x.title,
                score=x.score,
                score_total=x.score_total,
                    selected_answer_ids=(
                    x.selected_answer_ids.split(", ") if x.selected_answer_ids else []
                ),
                ordered_answer_pairs=(
                    json.loads(x.ordered_answer_pairs) if x.ordered_answer_pairs else {}
                ),
            )
            for x in db_user.user_exams
        ]
        user = UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            stripe_customer_id=db_user.stripe_customer_id,
            is_paying=db_user.is_paying,
            login_attempts=db_user.login_attempts,
            locked=db_user.locked,
            user_exams=user_exams,
        )
        return LoginRes(access_token=access, refresh_token=refresh, user=user)

    def logout(access_token: str, db: Session):
        payload = decodeJWT(access_token)
        user_id = payload["sub"]
        token_record = db.query(models.TokenTable).all()
        info = []
        for record in token_record:
            print("record", record)
            if (datetime.datetime.now() - record.created_date).days > 1:
                info.append(record.user_id)
        if info:
            print(info)
            existing_token = (
                db.query(models.TokenTable)
                .where(models.TokenTable.user_id.in_(info))
                .delete()
            )
            db.commit()

        existing_token = (
            db.query(models.TokenTable)
            .filter(
                models.TokenTable.user_id == user_id,
                models.TokenTable.access_token == access_token,
            )
            .first()
        )
        if existing_token:
            existing_token.status = False
            db.add(existing_token)
            db.commit()
            db.refresh(existing_token)
        return LogoutRes(message="Logout Successfully")

    def refresh_access_token_via_refresh_token(obj_in: TokenRefreshReq, db: Session):
        print(
            "refresh token for: ", obj_in.user_id, "with token: ", obj_in.refresh_token
        )
        if not obj_in.refresh_token:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect refresh token",
            )
        if not jwt_bearer.verify_refresh_jwt(obj_in.refresh_token):
            token_db = (
                db.query(models.TokenTable)
                .filter(models.TokenTable.user_id == user_id)
                .first()
            )
            setattr(token_db, "status", False)
            db.add(token_db)
            db.commit()
            db.refresh(token_db)
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token"
            )

        payload = decodeRefreshJWT(obj_in.refresh_token)
        user_id: str = payload.get("sub")
        access = create_access_token(user_id)
        token_db = (
            db.query(models.TokenTable)
            .filter(models.TokenTable.user_id == user_id)
            .first()
        )
        setattr(token_db, "access_token", access)
        db.add(token_db)
        db.commit()
        db.refresh(token_db)
        return TokenRefreshRes(access_token=access)

    def get_user(db: Session, user_id: int):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        print("########got user")
        print(user)
        return user

    def get_current_user(token: str, db: Session):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthErrorEnum.could_not_validate_credentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = decodeJWT(token)
            print(payload)
            user_id: str = payload.get("sub")
            if not user_id:
                raise credentials_exception
            token_data = TokenData(user_id=user_id)
        except JWTError:
            raise credentials_exception
        user = Auth.get_user(db, user_id=token_data.user_id)
        print(user)
        if user is None:
            raise credentials_exception
        return user
