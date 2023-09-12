from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from pydantic import BaseSettings
from models.users import User
from models.events import Event


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):  # 데이터베이스를 초기화하는 메서드를 정의한다.
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(  # db 클라이언트를 설정한다. SQLModel에서 생성한 몽고 엔진 버전과 문서 모델을 인수로 설정한다.
            database=client.get_default_dadtabase(),
            document_models=[Event, User],
        )

    class Config:  # db URL을 .env 파일에서 읽어온다.
        env_file = ".env"
