from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..crud.question import (
    create_question,
    delete_question,
    get_question,
    list_questions,
)
from ..crud.answer import (
    create_answer,
    get_answer,
    delete_answer,
)
from ..schemas.question import QuestionCreate, QuestionOut, QuestionWithAnswersOut
from ..schemas.answer import AnswerCreate, AnswerOut


api_router = APIRouter()


@api_router.get("/questions/", response_model=list[QuestionOut])
def api_list_questions(db: Session = Depends(get_db)):
    return list_questions(db)


@api_router.post("/questions/", response_model=QuestionOut, status_code=status.HTTP_201_CREATED)
def api_create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    return create_question(db, payload)


@api_router.get("/questions/{question_id}", response_model=QuestionWithAnswersOut)
def api_get_question(question_id: int, db: Session = Depends(get_db)):
    question = get_question(db, question_id, with_answers=True)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


@api_router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_question(question_id: int, db: Session = Depends(get_db)):
    deleted = delete_question(db, question_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return None


@api_router.post("/questions/{question_id}/answers/", response_model=AnswerOut, status_code=status.HTTP_201_CREATED)
def api_create_answer(question_id: int, payload: AnswerCreate, db: Session = Depends(get_db)):
    answer = create_answer(db, question_id, payload)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return answer


@api_router.get("/answers/{answer_id}", response_model=AnswerOut)
def api_get_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = get_answer(db, answer_id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return answer


@api_router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_answer(answer_id: int, db: Session = Depends(get_db)):
    deleted = delete_answer(db, answer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return None
