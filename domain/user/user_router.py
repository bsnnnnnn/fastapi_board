from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer # python-multipart 라이브러리 설치
from jose import jwt, JWTError # "python-jose[cryptography]" 라이브러리 설치
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

# 토큰 생성 시 필요한 정보
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 토큰 유효기간. 분 단위
SECRET_KEY = "a4a43e8d25f1d70050a602282be614d8879348bc11493704f36e575b0b400994" # 암호화시 사용하는 64자리 랜덤한 문자열
ALGORITHM = "HS256" # 토큰 생성 시 사용하는 알고리즘. HS256
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login") # 로그인 api의 url

router = APIRouter(
    prefix="/api/user",
)

# 유저 생성
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    # 이미 존재하는 유저인 경우(중복 확인)
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

# 로그인
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), # 로그인 api 입력 항목 가져오기
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username) # username 사용해 사용자 모델 객체(user) 조회해 가져오기
    # 입력 받은 비밀번호 암호화해 db에 저장된 암호와 일치하는지 확인
    if not user or not pwd_context.verify(form_data.password, user.password): # 해당 사용자를 찾지 못하거나 비밀번호가 일치하지 않으면
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED, # 401 : 사용자 인증 오류
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}, # 인증 방식에 대한 추가 정보
        )

    # make access token 액세스 토큰 생성 - jwt 사용
    # jwt : Json 포맷을 이용하여 사용자에 대한 속성을 저장하는 Claim 기반의 Web Token
    data = {
        "sub": user.username, # 사용자명
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

# 헤더 정보의 토큰값으로 사용자 정보 조회
def get_current_user(token: str = Depends(oauth2_scheme), # security 패키지의 OAuth2PasswordBearer에 의해 자동으로 매핑
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # 토큰을 복호화해 토큰에 담겨있는 사용자명을 얻을 수 있음
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError: # 사용자명이 없거나 해당 사용자명으로 데이터 조회에 실패할 경우
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user