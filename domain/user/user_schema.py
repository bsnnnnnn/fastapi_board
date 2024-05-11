from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr # 이메일 형식과 일치하지 않으면 오류 발생 # email_validator 설치해야 사용 가능

    @field_validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2') # password1, 2가 동일한지 확인
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

# 로그인 입력 스키마는 fastapi의 security 패키지에 있는 OAuth2PasswordRequestForm 클래스를 사용
# 로그인 출력 스키마
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

# User 모델
class User(BaseModel):
    id: int
    username: str
    email: str