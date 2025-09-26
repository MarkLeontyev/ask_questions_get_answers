from datetime import datetime

from pydantic import BaseModel, Field
from .answer import AnswerOut


class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class QuestionCreate(QuestionBase):
    pass


class QuestionOut(QuestionBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class QuestionWithAnswersOut(QuestionOut):
    answers: list[AnswerOut] = []

    model_config = {
        "from_attributes": True,
    }
