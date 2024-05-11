from datetime import datetime

from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreate, AnswerUpdate
from models import Question, Answer, User

# 답변 데이터를 db에 저장
def create_answer(db: Session, question: Question, answer_create: AnswerCreate, user: User):
    db_answer = Answer(question=question,
                       content=answer_create.content,
                       create_date=datetime.now(),
                       user=user) # user 모델의 객체 받아 저장
    db.add(db_answer)
    db.commit()

# 답변 조회 : answer_id와 일치하는 답변 조회해 리턴
def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id) 

# 답변 수정
def update_answer(db: Session, db_answer: Answer,
                  answer_update: AnswerUpdate):
    db_answer.content = answer_update.content
    db_answer.modify_date = datetime.now()
    db.add(db_answer)
    db.commit()

# 답변 삭제
def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()

# 답변 추천
def vote_answer(db: Session, db_answer: Answer, db_user: User):
    db_answer.voter.append(db_user)
    db.commit()