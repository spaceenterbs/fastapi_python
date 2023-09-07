from fastapi import APIRouter, Path
from models import Todo, TodoItem

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


@todo_router.get("/todo/{todo_id}")  # todo_id를 경로 매개변수로 추가한다.
async def get_single_todo(
    todo_id: int = Path(
        ..., title="The ID of the todo to retrieve."
    )  # Path는 라우트 함수에 있는 "다른 인수와 경로 매개변수를 구분"하는 역할을 한다.
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo,
            }
    return {
        "message": "Todo with supplied ID doesn't exist.",
    }


@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., title="The ID of the todo to be updated."),
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "Todo updated successfully.",
            }
    return {
        "message": "Todo with supplied ID doesn't exist.",
    }


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
        return {
            "message": "Todo deleted successfully.",
        }
    return {
        "message": "Todo with supplied ID doesn't exist.",
    }


@todo_router.delete("/todo")
async def delete_all_todos() -> dict:
    todo_list.clear()
    return {
        "message": "Todos deleted successfully.",
    }
