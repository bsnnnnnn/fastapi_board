# import contextlib

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# db 접속 주소
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

# 커넥션 풀(db에 접속하는 객체를 일정 갯수만큼 만들어놓고 돌려가며 사용) 생성
# db에 접속하는 세션 수 제어, 세션 접속에 소요되는 시간 줄임
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# db에 접속하기 위해 필요한 클래스
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# autocommit=False면 rollback 사용 가능. True면 불가능

# db 모델 구성에 사용되는 클래스
Base = declarative_base()
# db 제약조건 이름을 수동으로 설정
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

# Dependency Injection 의존성 주입
# db 세션 객체 리턴 제너레이터
# @contextlib.contextmanager # depends 사용 시 제거하기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()