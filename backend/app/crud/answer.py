from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.answers import Answer
from ..models.questions import Question
from ..schemas.answer import AnswerCreate


def create_answer(db: Session, question_id: int, data: AnswerCreate) -> Answer | None:
    question = db.get(Question, question_id)
    if not question:
        return None
    answer = Answer(question_id=question_id, user_id=data.user_id, text=data.text)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def get_answer(db: Session, answer_id: int) -> Answer | None:
    return db.get(Answer, answer_id)


def delete_answer(db: Session, answer_id: int) -> bool:
    answer = db.get(Answer, answer_id)
    if not answer:
        return False
    db.delete(answer)
    db.commit()
    return True


