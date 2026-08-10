from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}

# 조회를 위한 데이터 생성
todo_data = {
    1:{
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is_done": True,
    },
    2:{
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": False,
    },
    3:{
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False,
    },
}

# 전체 데이터 조회, 쿼리 파라미터 추가
@app.get("/todos")
# 쿼리 파라미터: str 또는 None
def get_todos_handler(order: str | None = None):
    ret = list(todo_data.values())
    # 쿼리 파라미터 값이 "DESC"인 경우 결과 역정렬 후 리턴
    if order and order == "DESC":
        return ret[::-1]
    # 아닌 경우, 바로 리턴
    return ret

#todos 아래에 {todo_id} path와 매핑
@app.get("/todos/{todo_id}")
# 입력 받은 {todo_id} 값으로 데이터 조회
def get_todo_handler(todo_id: int):
    return todo_data.get(todo_id, {})

# request body 검증을 위한 pydantic model 설계
class CreateToDoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

# 데이터 생성
@app.post("/todos")
# request pydantic 검증 후 
def create_todo_handler(request: CreateToDoRequest):
    # 새로운 데이터로 추가
    todo_data[request.id] = request.dict()
    # 추가한 데이터 리턴
    return todo_data[request.id]

# {todo_id}에 해당하는 데이터 수정
@app.patch("/todos/{todo_id}")
def update_todo_handler(
    todo_id: int,
    # request body 하나의 컬럼 값을 사용할 수 있음
    is_done: bool = Body(..., embed=True)
):
    todo = todo_data.get(todo_id)
    # todo가 있다면
    if todo:
        # request 값으로 수정
        todo["is_done"] = is_done
        return todo
    # todo가 없다면
    return {}

# 데이터 삭제
@app.delete("/todos/{todo_id}")
def delete_todo_handler(todo_id: int):
    # {todo_id}에 해당하는 데이터 삭제, 키 에러 방지(None: default value)
    todo_data.pop(todo_id, None)
    return todo_data