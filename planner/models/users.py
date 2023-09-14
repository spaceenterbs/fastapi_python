# 사용자 처리용 모델을 정의
from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from models.events import Event


class User(Document):
    email: EmailStr
    password: str
    # events: Optional[
    #     List[Event]
    # ]  # 선택적 필드인 Optional은 필요에 따라 값을 포함하거나 생략할 수 있다. None이 될 수 있다. # = None  # 기본값을 정해줘야 한다.

    class Settings:
        name = "users"

    # model_config = {
    #     "json_schema_extra": {
    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "strong!!!",
                # "events": [],
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZh",
    #             "token_type": "bearer ",
    #         }
    #     }


# class UserSignIn(Document):  # "로그인 라우트 변경"과 함께 더 이상 사용되지 않게 된다.
#     email: EmailStr
#     password: str

#     # model_config = {
#     #     "json_schema_extra": {
#     class Config:
#         schema_extra = {
#             "example": {
#                 "email": "fastapi@packt.com",
#                 "password": "strong!!!",
#                 "events": [],
#             }
#         }
