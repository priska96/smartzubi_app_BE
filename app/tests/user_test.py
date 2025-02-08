from .utils import client
import pytest


@pytest.mark.usefixtures("reset_database")
class TestUserEndpoints:
    def test_get_user(self):
        response = client.get("/api/user/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["username"] == "defaultuser"
        assert data["email"] == "default@example.com"
        assert data["is_paying"] == False
        assert data["stripe_customer_id"] == None
        assert data["user_exams"] != []

    def test_create_user(self):
        response = client.post(
            "/api/register",
            json={
                "username": "johndoe",
                "password": "123456",
                "email": "john@example.com",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert data["user_id"] == 2

    def test_patch_user(self):
        response = client.patch("/api/user/1", json={"is_paying": True})
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "defaultuser"
        assert data["is_paying"] == True

    def test_get_user_not_found(self):
        response = client.get("/api/user/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User with id: 999 not found"}

    def test_create_user_exam(self):
        response = client.post(
            "/api/user/1/exam/create",
            json={
                "exam_id": 1,
                "user_id": 1,
                "title": "Exam 2025",
                "answered_questions": [
                    {
                        "question_id": 1,
                        "answer_ids": [1, 2],
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
                        "answer_pair": {
                            "6": "2",
                            "7": "1",
                            "8": "3",
                            "9": "5",
                            "10": "4",
                        },
                        "type": "ordering",
                    },
                    {
                        "question_id": 4,
                        "answer_ids": [2],
                        "answer_pair": {},
                        "type": "multiple_choice",
                    },
                ],
            },
        )
        assert response.status_code == 200
        data = response.json()
        print(data)
        assert data["exam_id"] == 1
        assert data["user_id"] == 1
        assert data["score"] == 4
        assert data["score_total"] == 6

    def test_get_user_exam(self):
        response = client.get("/api/user/1/exam/1")
        assert response.status_code == 200
