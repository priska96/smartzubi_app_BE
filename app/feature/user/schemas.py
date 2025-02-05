import datetime
from typing import List, Optional, Union
from ... import models
from pydantic import BaseModel


class UserExam(BaseModel):
    id: int
    created_at: datetime.datetime
    title: str
    exam_id: int
    score: int
    score_total: int
    selected_answer_ids: str
    ordered_answer_pairs: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_paying: bool
    stripe_customer_id: Optional[str] = ""
    user_exams: Union[List[UserExam], None] = []
    login_attempts: int
    locked: bool

    class ConfigDict:
        from_attributes = True

class UserPatchReq(BaseModel):
    email: Optional[str] = None
    is_paying: Optional[bool] = None
    password: Optional[str] = None
    stripe_customer_id: Optional[str] = None


class AnsweredQuestions(BaseModel):
    question_id: int
    answer_ids: Union[List[int], None]
    answer_pair: Union[dict, None]
    type: models.TypeEnum


class UserExamCreateReq(BaseModel):
    user_id: int
    exam_id: int
    title: str
    answered_questions: List[AnsweredQuestions]


class UserExamCreateRes(BaseModel):
    user_id: int
    exam_id: int
    score: int
    score_total: int
    selected_answer_ids: List[int]
    ordered_answer_pairs: dict


class UserExamRes(BaseModel):
    id: int
    created_at: datetime.datetime
    title: str
    exam_id: int
    score: int
    score_total: int
    selected_answer_ids: List[int] = []
    ordered_answer_pairs: dict
