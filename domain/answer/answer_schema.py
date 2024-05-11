import datetime

from pydantic import BaseModel, field_validator
from domain.user.user_schema import User

# 답변 등록
class AnswerCreate(BaseModel):
    content: str

    # 빈 문자열 허용 안함
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip(): # 빈 값인 경우 오류 발생
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

# 답변 표시
class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None
    voter: list[User] = [] # 추천인

# 답변 수정
class AnswerUpdate(AnswerCreate):
    answer_id: int

# 답변 삭제
class AnswerDelete(BaseModel):
    answer_id: int

# 답변 추천
class AnswerVote(BaseModel):
    answer_id: int