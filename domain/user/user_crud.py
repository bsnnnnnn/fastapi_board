from passlib.context import CryptContext # 비밀번호 암호화
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# UserCreate 스키마로 회원 데이터 생성
def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1), # 비밀번호 암호화해 저장 
                   email=user_create.email)
    db.add(db_user)
    db.commit()
    # 이후 로그인 시 동일한 방식으로 암호화해 db에 저장된 값과 비교. 복호화 필요 없음

# 중복값에 대한 예외처리
# 입력항목 중 사용자명이나 이메일이 이미 존재하는지 확인
def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()

# 로그인 CRUD
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()