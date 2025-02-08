from typing import List
from enum import Enum
from .database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    DateTime,
    text,
    ForeignKey,
    LargeBinary,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
import datetime


class Exam(Base):
    __tablename__ = "exam"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    title = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    questions: Mapped[List["Question"]] = relationship(back_populates="exam")
    google_drive_link = Column(String, nullable=True)


class TypeEnum(Enum):
    multiple_choice = "multiple_choice"
    ordering = "ordering"
    calculation = "calculation"


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    title = Column(String, nullable=False)
    question = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    type = Column(ENUM(TypeEnum), nullable=False, default=TypeEnum.multiple_choice)
    hint = Column(String, nullable=True)
    solution_hint = Column(String, nullable=True)
    answers: Mapped[List["Answer"]] = relationship(back_populates="question")
    exam_id: Mapped[int] = mapped_column(ForeignKey("exam.id"), nullable=True)
    exam: Mapped["Exam"] = relationship(back_populates="questions")


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    answer = Column(String, nullable=False)
    correct = Column(Boolean, server_default="TRUE")
    correct_order = Column(Integer, nullable=True)
    points = Column(Integer, nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=True)
    question: Mapped["Question"] = relationship(back_populates="answers")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(LargeBinary(100), nullable=False)
    is_paying = Column(Boolean, server_default="FALSE")
    stripe_customer_id = Column(String(300), nullable=True)
    user_exams: Mapped[List["UserExam"]] = relationship(back_populates="user")
    device: Mapped["Device"] = relationship(back_populates="user")
    login_attempts = Column(Integer, server_default="0", nullable=False)
    locked = Column(Boolean, server_default="FALSE")


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)


class UserExam(Base):
    __tablename__ = "userexam"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    exam_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    score_total = Column(Integer, nullable=False)
    selected_answer_ids = Column(String(100), nullable=False)
    ordered_answer_pairs = Column(String(150), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="user_exams")


class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="device")
