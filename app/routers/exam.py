from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..feature.auth.auth_bearer import jwt_bearer
from ..api_wrappers import paying_member_required, token_required
from ..feature.exam.schemas import (
    QuestionCreateReq,
    QuestionRes,
    ExamCreateReq,
    ExamRes,
    ExamGetRes,
)
from ..feature.exam.question_api import Question
from ..feature.exam.exam_api import Exam

# Create an APIRouter instance
router = APIRouter(prefix="/api", tags=["exam"])


@router.post("/questions", status_code=201, response_model=QuestionRes)
@token_required
async def create_question(obj_in: QuestionCreateReq, db: Session = Depends(get_db)):
    return Question.create(obj_in, db)


@router.post("/exam", status_code=201, response_model=ExamRes)
@token_required
async def create_exam(obj_in: ExamCreateReq, db: Session = Depends(get_db)):
    return Exam.create(obj_in, db)


@router.get("/exam/{exam_id}", status_code=200, response_model=ExamGetRes)
@token_required
#@paying_member_required
async def get_exam(
    exam_id: int, db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)
):
    return Exam.get_by_id(exam_id, db)


@router.get("/exam", status_code=200, response_model=List[ExamGetRes])
@token_required
#@paying_member_required
async def get_all_exams(
    db: Session = Depends(get_db), dependencies=Depends(jwt_bearer)
):
    return Exam.get(db)
