from fastapi import APIRouter
from models import Todo

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo")
async def add_todo(todo: Todo) -> dict:  # 요청 바디의 변수 유형을 dict에서 Todo로 변경한다.
    todo_list.append(todo)
    return {
        "message": "Todo added successfully.",
    }


@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list,
    }
