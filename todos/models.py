from pydantic import BaseModel
from typing import List


class Todo(BaseModel):
    id: int
    item: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "item": "Example Schema!",
            }
        }
    }


class TodoItem(BaseModel):  # UPDATE 라우트 요청 바디용 모델
    item: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "item": "Read the next chapter of the book.",
            }
        }
    }


class TodoItems(BaseModel):
    todos: List[TodoItem]

    model_config = {
        "json_schema_extra": {
            "example": {
                "todos": [
                    {
                        "item": "Example Schema 1!",
                    },
                    {
                        "item": "Example Schema 2!",
                    },
                ]
            }
        }
    }
