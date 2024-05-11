from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

# 질문 추천 기능 - many to many 관계 : 한 명의 사용작가 여러 개의 질문을 추천하거나 한 개의 질문을 여러 명이 추천할 수 있음
# user_id, questio_id가 둘 다 같은 경우는 중복 불가
question_voter = Table(
    'question_voter', # 테이블명
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

# 답변 추천 기능
answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)

# 질문 모델
class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True) # user 모델과 연결
    user = relationship("User", backref="question_users") # question 모델에서 user 모델 참조하기 위한 속성
    modify_date = Column(DateTime, nullable=True) # 수정 일시
    voter = relationship('User', secondary=question_voter, backref='question_voters')

# 답변 모델
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id")) # 질문 id 컬럼과 연결
    question = relationship("Question", backref="answers") # 답변 모델에서 질문 모델 참조 # (참조할 모델명, 역참조 설정)
    # backref 역참조 : 질문에서 답변을 거꾸로 참조. 이름 중복 사용 불가
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True) # 수정 일시
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')

# 유저 모델
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)