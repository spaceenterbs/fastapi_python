# 이벤트 처리용 모델을 정의
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import JSON, SQLModel, Field, Column


# models/events.py에 정의한 Event 모델 클래스를 변경해서 SQLModel 테이블 클래스를 사용하도록 만든다.
class Event(SQLModel, table=True):  # 기존 모델 클래스를 SQL 테이블 클래스로 변경한다.
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    # class Event(BaseModel):
    #     id: int
    #     title: str
    #     image: str
    #     description: str
    #     tags: List[str]
    #     location: str

    # model_config = {
    #     "arbitrary_types_allowed": True,
    #     "json_schema_extra": {
    class Config:
        arbitrary_types_allowed: True
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "Wewill be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
            },
        }


# UPDATE 처리의 바디 유형으로 사용할 SQLModel 클래스를 추가한다.
class EventUpdate(SQLModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    # model_config = {
    #     "json_schema_extra": {

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet",
            },
        }
