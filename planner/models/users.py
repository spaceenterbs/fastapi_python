# 사용자 처리용 모델을 정의
from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: Optional[  # 선택적 필드인 Optional은 필요에 따라 값을 포함하거나 생략할 수 있다. None이 될 수 있다.
        List[Event]
    ] = None  # 기본값을 정해줘야 한다.

    # model_config = {
    #     "json_schema_extra": {
    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "strong!!!",
                "events": [],
            }
        }

    class Settings:
        name = "users"


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    # model_config = {
    #     "json_schema_extra": {
    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": [],
            }
        }
