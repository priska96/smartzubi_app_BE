from typing import Dict, List, Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db

from ..api_wrappers import paying_member_required, token_required
from ..feature.auth.auth_bearer import jwt_bearer
from ..feature.user.schemas import (
    UserResponse,
    UserExamCreateReq,
    UserExamCreateRes,
    UserExamRes,
    UserPatchReq,
)
from ..feature.user.user_api import User


# Create an APIRouter instance
router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/{user_id}", status_code=200, response_model=Union[UserResponse, Dict])
@token_required
async def get_user(
    user_id: int, db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)
) -> UserResponse:
    print("gere", db)
    return User.get(user_id, db)


@router.patch("/{user_id}", status_code=200, response_model=UserResponse)
async def update_user(
    user_id: int, obj_in: UserPatchReq, db: Session = Depends(get_db)
):
    return User.update(user_id, obj_in, db)


@router.post(
    "/{user_id}/exam/create", status_code=200, response_model=UserExamCreateRes
)
@token_required
@paying_member_required
async def create_exam_for_user(
    user_id: int,
    obj_in: UserExamCreateReq,
    db: Session = Depends(get_db),
    dependencies=Depends(jwt_bearer),
):
    print("stasrt")
    return User.create_user_exam(obj_in, db)


@router.get(
    "/{user_id}/exam/{user_exam_id}",
    status_code=200,
    response_model=UserExamRes,
)
@token_required
@paying_member_required
async def get_user_exam(
    user_id: int,
    user_exam_id: int,
    db: Session = Depends(get_db),
    dependencies=Depends(jwt_bearer),
):
    return User.get_user_exam(user_exam_id, db)


@router.get("/{user_id}/exam", status_code=200, response_model=List[UserExamRes])
@token_required
@paying_member_required
async def get_user_all_user_exams(
    user_id: int, db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)
):
    return User.get_all_user_exams(user_id, db)
