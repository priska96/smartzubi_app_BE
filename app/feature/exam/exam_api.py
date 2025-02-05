import random
from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect
from sqlalchemy.orm import RelationshipProperty, Session

from ... import models
from .schemas import ExamCreateReq
from .question_api import Question


class Exam:
    def create(obj_in: ExamCreateReq, db: Session):
        def object_as_dict(obj, relationships=False):
            """
            Converts an SQLAlchemy instance to a dictionary.

            :param relationships: If true, also include relationships in the output dict
            """
            obj_dict = jsonable_encoder(obj, exclude_defaults=True)
            properties = inspect(models.Exam).mapper.all_orm_descriptors

            if not relationships:
                return {
                    key: obj_dict[key]
                    for key, value in properties.items()
                    if (
                        not hasattr(value, "prop")
                        or not isinstance(value.prop, RelationshipProperty)
                    )
                    and key in obj_dict
                }
            else:
                return {
                    key: obj_dict[key]
                    for key, value in properties.items()
                    if key in obj_dict
                }

        obj_in_dict = jsonable_encoder(obj_in, exclude_defaults=True)
        # print(obj_in_dict,"\n\n")
        obj_in_parent = object_as_dict(obj_in_dict)
        obj_in_data = object_as_dict(obj_in_dict, relationships=True)
        # print(obj_in_parent,"\n\n", obj_in_data,"\n\n")
        db_obj = models.Exam(**obj_in_parent)  # type: ignore
        db.add(db_obj)
        db.commit()

        db.refresh(db_obj)
        print("###### created Exam")
        db_questions = []
        for question in obj_in.questions:
            db_question = Question.create(question, db)
            setattr(db_question, "exam_id", db_obj.id)
            setattr(db_question, "exam", db_obj)
            db_questions.append(db_question)
            print(db_question, "\n\n")

        setattr(db_obj, "questions", db_questions)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(exam_id: int, db: Session):
        exam = db.get(models.Exam, exam_id)
        random.shuffle(exam.questions)
        return exam

    def get(db: Session):
        return db.query(models.Exam).all()
