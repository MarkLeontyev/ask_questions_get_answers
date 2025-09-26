from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from ..models.questions import Question
from ..models.answers import Answer
from ..schemas.question import QuestionCreate


def create_question(db: Session, data: QuestionCreate) -> Question:
    question = Question(text=data.text)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question(db: Session, question_id: int, with_answers: bool = False) -> Question | None:
    if with_answers:
        stmt = select(Question).options(joinedload(Question.answers)).where(Question.id == question_id)
        return db.scalars(stmt).first()
    return db.get(Question, question_id)


def list_questions(db: Session) -> list[Question]:
    stmt = select(Question).order_by(Question.id.desc())
    return list(db.scalars(stmt).all())


def delete_question(db: Session, question_id: int) -> bool:
    question = db.get(Question, question_id)
    if not question:
        return False
    db.delete(question)
    db.commit()
    return True
