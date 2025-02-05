import datetime
import json
import string
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ... import models
from ...database import engine

from app.feature.user.schemas import (
    UserPatchReq,
    UserExamCreateReq,
    UserExamCreateRes,
    UserExamRes,
)


class User:
    def get(user_id: int, db: Session):
        print("db", db)
        maybe_user = db.get(models.User, user_id)
        if not maybe_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {user_id} not found",
            )
        print("maybe_user", maybe_user)
        return db.get(models.User, user_id)

    def update(user_id: int, obj_in: UserPatchReq, db: Session):
        db_user = db.get(models.User, user_id)
        for key, value in obj_in.model_dump().items():
            if value:
                setattr(db_user, key, value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def create_user_exam(obj_in: UserExamCreateReq, db: Session):
        exam_score = db.get(models.Exam, obj_in.exam_id).score

        score = 0
        selected_answer_ids = []
        ordered_pairs = {}

        for answered in obj_in.answered_questions:
            question_points = db.get(models.Question, answered.question_id).points
            if answered.type == models.TypeEnum.multiple_choice:
                score = User.count_points_multiple_choice_question(
                    answered, score, db, selected_answer_ids, question_points
                )
            if answered.type == models.TypeEnum.ordering:
                score = User.count_points_ordering_question(
                    answered, db, score, ordered_pairs
                )
            if answered.type == models.TypeEnum.calculation:
                score = User.count_points_calculation_question(
                    answered, db, score, ordered_pairs
                )
        selected_ids_str = ", ".join([str(i) for i in selected_answer_ids])
        print(selected_ids_str)

        print("##########final score:", score)
        user_exam_db = models.UserExam(
            **{
                "user_id": obj_in.user_id,
                "exam_id": obj_in.exam_id,
                "created_at": datetime.datetime.now(datetime.UTC),
                "title": obj_in.title,
                "score": score,
                "score_total": exam_score,
                "selected_answer_ids": selected_ids_str,
                "ordered_answer_pairs": json.dumps(ordered_pairs),
            }
        )
        print("user_exam_id", user_exam_db.id)
        db.add(user_exam_db)
        db.commit()
        db.refresh(user_exam_db)
        return UserExamCreateRes(
            user_id=obj_in.user_id,
            exam_id=obj_in.exam_id,
            score=score,
            score_total=exam_score,
            selected_answer_ids=selected_answer_ids,
            ordered_answer_pairs=ordered_pairs,
        )

    def count_points_multiple_choice_question(
        answered, score, db, selected_answer_ids, question_points
    ):
        correctly_answered = db.query(models.Answer).filter(models.Answer.id.in_(answered.answer_ids)).all()

        for answer_db in correctly_answered:
            if answer_db.correct:
                score += answer_db.points
                print("answer correct. curr points: ", score)
            selected_answer_ids.append(answer_db.id)
        print("points", question_points)
        return score

    def count_points_ordering_question(answered, db, score, ordered_pairs):
        correct_order = db.query(models.Answer).filter(
            models.Answer.question_id == answered.question_id
        ).all()
        for answer_db in correct_order:
            answer_db: models.Answer
            str_answer_id = str(answer_db.id)
            print(
                "answer_pair: ",
                answered.answer_pair,
                answered.answer_pair[str_answer_id],
            )
            print("answer_db.correct_order: ", answer_db.correct_order)
            order_user = int(answered.answer_pair[str(answer_db.id)])
            if (
                order_user == answer_db.correct_order
            ):  # user's order is same as correct order
                print("correct order")
                score += answer_db.points
                print("##########current score:", score)
            ordered_pairs[answer_db.id] = answered.answer_pair[str_answer_id]
        return score

    def count_points_calculation_question(answered, db, score, ordered_pairs):
        correct_order = db.query(models.Answer).filter(
            models.Answer.question_id == answered.question_id
        ).all()

        for answer_db in correct_order:
            answer_db: models.Answer
            str_answer_id = str(answer_db.id)
            print(
                "answer_pair: ",
                answered.answer_pair,
                answered.answer_pair[str_answer_id],
            )
            cleaned_answer_user = answered.answer_pair[str(answer_db.id)].translate(
                {ord(c): None for c in string.whitespace}
            )
            cleaned_answer = answer_db.answer.translate(
                {ord(c): None for c in string.whitespace}
            )
            if (
                cleaned_answer_user == cleaned_answer
            ):  # user's answer is same as correct answer
                print("correct calculation")
                score += answer_db.points
                print("##########current score:", score)
            ordered_pairs[answer_db.id] = answered.answer_pair[str_answer_id]
        return score

    def get_user_exam(user_exam_id: int, db: Session):
        user_exam_db = db.get(models.UserExam, user_exam_id)
        print("user_exam_db.ordered_answer_pairs ", db.query(models.UserExam).all())  
        return UserExamRes(
                id=user_exam_db.id,
                exam_id=user_exam_db.exam_id,
                created_at=user_exam_db.created_at,
                title=user_exam_db.title,
                score=user_exam_db.score,
                score_total=user_exam_db.score_total,
                selected_answer_ids=(
                    user_exam_db.selected_answer_ids.split(", ")
                    if user_exam_db.selected_answer_ids
                    else []
                ),
                ordered_answer_pairs=json.loads(user_exam_db.ordered_answer_pairs),
            ) if user_exam_db.ordered_answer_pairs else {}
        

    def get_all_user_exams(user_id: int, db: Session):
        user_exams_db = (
            db.query(models.UserExam).filter(models.UserExam.user_id == user_id).all()
        )
        res = [
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
            for x in user_exams_db
        ]
        return res
