from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from sqlalchemy import and_ # sqlalchemy outer join
from models import Question, User, Answer
from sqlalchemy.orm import Session

# 질문 목록
def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''): # skip : 조회한 데이터의 시작 위치, limit: 시작 위치부터 가져올 데이터의 건수, keyword : 검색 키워드
    question_list = db.query(Question)
    # 검색 기능
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |        # 질문제목
                    Question.content.ilike(search) |        # 질문내용
                    User.username.ilike(search) |           # 질문작성자
                    sub_query.c.content.ilike(search) |     # 답변내용
                    sub_query.c.username.ilike(search)      # 답변작성자
                    ) # 각 항목에서 or 조건으로 검색
    total = question_list.distinct().count() # offset, limit 적용 전에 먼저 구해야 함
    question_list = question_list.order_by(Question.create_date.desc())\
        .offset(skip).limit(limit).distinct().all()
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)

# id에 해당하는 질문 조회해 리턴
def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

# 질문 데이터 저장
def create_question(db: Session, question_create: QuestionCreate, user:User):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now(),
                           user=user)
    db.add(db_question)
    db.commit()

# 질문 수정
def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()

# 질문 삭제
def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()

# 질문 추천
def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()