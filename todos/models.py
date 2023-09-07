from pydantic import BaseModel


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
