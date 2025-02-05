
import pytest
import os
import json
from .utils import TestingSessionLocal, engine, Base
from .. import models
from ..feature.auth.utils import get_hashed_password
from ..feature.exam.schemas import ExamCreateReq
from ..feature.exam.exam_api import Exam
from ..feature.user.user_api import User
from ..feature.user.schemas import UserExamCreateReq


# Define a pytest fixture to flush the database between tests
@pytest.fixture(scope="function")
def reset_database():
    # Drop all tables before the test
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables before the test
    Base.metadata.create_all(bind=engine)
    # Insert a default user into the test database

    current_directory = os.getcwd()
    files = [current_directory + "/app/fixtures/notion_temp.json"]
    with TestingSessionLocal() as db:
        try:
            default_user = models.User(
                username="defaultuser",
                password=get_hashed_password("123456"),
                email="default@example.com",
                is_paying=False,
            )
            db.add(default_user)
            db.commit()
        finally:
            db.close()  # Close the session explicitly

    with open(files[0], "r") as json_file:
        data = json.load(json_file)
    with TestingSessionLocal() as db:    
        try:
            Exam.create(ExamCreateReq(**data), db)
            user_exam_json = {
                "exam_id": 1,
                "user_id": 1,
                "title": "Exam 2025",
                "answered_questions": [
                    {
                        "question_id": 1,
                        "answer_ids": [1,2],
                        "answer_pair": {},
                        "type": "multiple_choice",
                    },
                    {
                        "question_id": 2,
                        "answer_ids": [],
                        "answer_pair": {"5": "130x130"},
                        "type": "calculation",
                    },
                    {
                        "question_id": 3,
                        "answer_ids": [],
                        "answer_pair": {"6": "2", "7": "1", "8": "3", "9": "5", "10": "4"},
                        "type": "ordering",
                    },
                    {
                        "question_id": 4,
                        "answer_ids": [2],
                        "answer_pair": {},
                        "type": "multiple_choice",
                    },
                ],
            }
            User.create_user_exam(UserExamCreateReq(**user_exam_json), db)
        finally:
            db.close()  # Close the session explicitly

    yield
    # Drop all tables after the test (optional but good for cleaning)
    Base.metadata.drop_all(bind=engine)
