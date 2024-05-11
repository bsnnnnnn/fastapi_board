from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# 프론트엔드 빌드
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

app = FastAPI()

origins = [
    "http://localhost:5173",    # 또는 "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get('/hello') # /hello url 요청 발생 시 해당 함수 실행
# def hello():
#     return {"message": "안녕"}

app.include_router(question_router.router) # question_router.py의 라우터 객체 등록
app.include_router(answer_router.router) # 답변 등록 라우터 등록
app.include_router(user_router.router) # 회원가입 라우터 등록
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

# 프론트엔드 빌드 통해 생성한 파일 서비스
@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html") # fastapi가 정적인 파일 출력 시 사용