import datetime
from pydantic import BaseModel, field_validator
from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

# 출력 항목 정의 및 타입 지정
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = [] # Answer 스키마로 구성된 리스트 
    user: User | None # question 모델을 question 스키마에 매핑할 때 자동으로 값 채워짐
    modify_date: datetime.datetime | None = None # default : None. 수정 발생할 때만 값 생성됨
    voter: list[User] = [] # 추천인
    # Question 모델의 항목들이 자동으로 Question 스키마로 매핑됨
    # class Config:
    #     # orm_mode = True
    #     from_attributes = True

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

# 질문 목록 api의 응답으로 사용할 스키마
class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

# 질문 수정
class QuestionUpdate(QuestionCreate): # questioncreate 상속
    question_id: int

# 질문 삭제
class QuestionDelete(BaseModel):
    question_id: int

# 질문 추천
class QuestionVote(BaseModel):
    question_id: int