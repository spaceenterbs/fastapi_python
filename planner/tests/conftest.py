import asyncio  # 활성 루프 세션을 만들어서 테스트가 단일 스레드로 실행되도록 한다.
import httpx  # httpx 테스트는 HTTP CRUD 처리를 실행하기 위한 비동기 클라이언트 역할을 한다.
import pytest  # 픽스처 정의를 위해 사용된다.

from main import app
from database.connection import Settings
from models.events import Event
from models.users import User


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# Settings 클래스에서 새로운 db 인스턴스를 만든다.
async def init_db():
    """DATABASE_URL과 초기화 함수를 호출하고. testdb라는 새로운 db를 사용한다."""
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

    await test_settings.initializer_database()


# 기본 클라이언트 픽스처를 정의한다. 이 픽스처는 httpx를 통해 비동기로 실행되는 앱 인스턴스를 반환한다.
@pytest.fixture(scope="session")  # AsyncClient는 테스트 세션이 끝날 때까지 유지된다.
async def default_client():
    await init_db()  # 테스트가 실행되기 전에 데이터베이스를 초기화한다.
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
        # 리소스 정리 = 테스트 세션이 끝나면 이벤트와 사용자 컬렉션의 데이터를 모두 삭제하여 테스트를 실행할 때마다 db가 축적되는 것을 방지한다.
        await Event.find_all().delete()
        await User.find_all().delete()
