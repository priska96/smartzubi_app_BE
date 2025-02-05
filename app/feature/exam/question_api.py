from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect
from sqlalchemy.orm import RelationshipProperty, Session

from ... import models
from .schemas import QuestionCreateReq


class Question:
    def create(obj_in: QuestionCreateReq, db: Session):
        def object_as_dict(obj: QuestionCreateReq, relationships=False):
            """
            Converts an SQLAlchemy instance to a dictionary.

            :param relationships: If true, also include relationships in the output dict
            """
            obj_dict = jsonable_encoder(obj, exclude_defaults=True)
            properties = inspect(models.Question).mapper.all_orm_descriptors

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
        obj_in_parent = object_as_dict(obj_in_dict)
        obj_in_data = object_as_dict(obj_in_dict, relationships=True)
        db_obj = models.Question(**obj_in_parent)  # type: ignore
        db.add(db_obj)
        db.commit()

        for key, value in obj_in_data.items():
            if key in obj_in_parent or not hasattr(models.Question, key):
                continue

            children = [
                getattr(models.Question, key).prop.entity._identity_class(
                    **child, question_id=db_obj.id
                )
                for child in value
            ]

            setattr(db_obj, key, children)

        db.commit()
        db.refresh(db_obj)
        return db_obj
