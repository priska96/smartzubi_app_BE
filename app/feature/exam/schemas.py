from typing import List, Union
from pydantic import BaseModel

from ... import models


class AnswerCreateReq(BaseModel):
    answer: str
    correct: bool
    correct_order: Union[int, None]
    points: int

    class Meta:
        orm_model = models.Answer


class AnswerRes(AnswerCreateReq):
    id: int

    class ConfigDict:
        from_attributes = True


class QuestionCreateReq(BaseModel):
    title: str
    question: str
    points: int
    type: models.TypeEnum
    hint: Union[str, None]
    solution_hint: Union[str, None]
    answers: List[AnswerCreateReq] = []


class QuestionRes(QuestionCreateReq):
    id: int

    class ConfigDict:
        from_attributes = True


class QuestionModelRead(QuestionRes):
    id: int
    answers: List[AnswerRes] = []

    class ConfigDict:
        from_attributes = True


class ExamCreateReq(BaseModel):
    title: str
    questions: List[QuestionCreateReq] = []
    score: int
    google_drive_link: Union[str, None]


class ExamRes(ExamCreateReq):
    id: int

    class ConfigDict:
        from_attributes = True


class ExamGetRes(ExamCreateReq):
    id: int
    questions: List[QuestionModelRead] = []

    class ConfigDict:
        from_attributes = True
