from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form


class Todo(BaseModel):
    id: Optional[int] = None
    item: str

    @classmethod
    def as_form(cls, item: str = Form(...)):
        return cls(item=item)

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
    todos: List[TodoItem]  # TodoItem 모델에 정의된 변수 목록을 반환한다.

    model_config = {
        "json_schema_extra": {
            "example": {
                "todos": [
                    {
                        "item": "Example Schema 1!",
                    },
                    {
                        "item": "Example Schema 2!!",
                    },
                ]
            }
        }
    }
