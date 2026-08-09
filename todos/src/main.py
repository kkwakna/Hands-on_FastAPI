from fastapi import FastAPI

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

# 전체 데이터 조회
@app.get("/todos")
def get_todos_handler():
    # 데이터의 값을 리스트에 담아서 리턴
    return list(todo_data.values())

