from datetime import datetime

from pydantic import BaseModel, Field


class AnswerBase(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1, max_length=5000)


class AnswerCreate(AnswerBase):
    pass


class AnswerOut(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
