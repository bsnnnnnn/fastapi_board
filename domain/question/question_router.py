from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

from starlette import status
# from models import Question

# 라우터 객체 생성 # fastapi 앱에 등록해야 라우팅 기능 동작 = fastapi가 요청 받은 url을 해석해 그에 맞는 함수 실행해 결과 리턴
router = APIRouter(
    prefix="/api/question", # 요청 url에 항상 포함되어야 하는 값
)

# 질문 목록
# question_list의 리턴값은 Question 스키마로 구성된 리스트
@router.get("/list", response_model=question_schema.QuestionList) # 출력 항목에 전체 건수 추가
def question_list(db: Session = Depends(get_db), # db 객체가 session 타입 # get_db 제너레이터에 의해 생성된 세션 객체가 주입됨
                  page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size, keyword=keyword) # 한 페이지에 보여줄 게시물 개수 추가
    return {
        'total': total,
        'question_list': _question_list
    }

# 질문 상세 조회 api
# question_id로 질문 상세 내역 조회, Question 스키마로 리턴
@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

# 질문 등록
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT) # 리턴할 응답이 없는 경우 204 리턴
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create, user=current_user)

# 질문 수정
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question: # 찾는 질문이 없는 경우
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id: # 질문 작성자와 현재 로그인한 사용자가 다른 경우
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    # 문제 없으면 질문 데이터 수정
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)
    
# 질문 삭제
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)

# 질문 추천
@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question: # 조회 결과가 없는 경우
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)