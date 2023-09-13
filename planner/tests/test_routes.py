import httpx
import pytest

from auth.jwt_handler import create_access_token  # create_access_token(user) 함수를 임포트한다.
from models.events import Event


# 몇몇 라우트는 보안이 적용되므로 접속 토큰을 생성해야 한다.
# 따라서 새로운 픽스처를 만들고 접속 토큰을 반환하도록 한다.
@pytest.fixture(scope="module")  # 테스트 파일이 실행될 때 한 번만 실행되고 다른 함수가 호출될 때는 실행되지 않는다.
async def access_token() -> str:
    return create_access_token("testuser@packt.com")


# 이벤트를 db에 추가하는 픽스처를 만든다.
# 이 픽스처는 CRUD 테스트에 대한 사전 테스트를 진행하는 데 사용된다.
@pytest.fixture(
    scope="module"
)  # 동일한 파일에서 모듈 단위로 한 번만 실행된다. mock_event 함수는 딱 한번만 호출되고 그 반환값은 같은 .py 파일 내의 모든 테스트 함수에서 재사용된다.
async def mock_event() -> Event:  # Event 객체를 생성한다.
    new_event = Event(  # 함수 내부에서 먼저 new_event 객체를 생성한다. 이 객체에는 각 필드에 대한 값이 포함된다.
        creator="testuser@packt.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png",
        description="We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
        tags=["python", "fastapi", "book", "launch"],
        location="Google Meet",
    )

    await Event.insert_one(
        new_event
    )  # 해당 이벤트 객체를 db에 추가한다. 여기서 await문은 비동기 함수의 실행을 기다리라는 의미이다.
    # 즉, 'insert_one' 메서드가 완료될 때까지 코드 실행을 일시 중지하고, 이후 코드를 실행한다.
    # db에 데이터를 삽입하는 데 시간이 걸릴 수 있으므로, 이 작업이 완료될 때까지 yield new_event를 실행하지 않도록 하는 것이다.

    yield new_event  # 생성된 이벤트 객체를 반환하고 함수 실행을 일시 중단합니다.

    # 목표 = 모듈 단위로 동일한 테스트용 이벤트 데이터를 생성하고 DB에 저장한 후 반환하는 것


# /event(이벤트 라우트)의 GET 메서드 테스트 함수를 작성한다.
@pytest.mark.asyncio
async def test_get_events(
    default_client: httpx.AsyncClient,
    mock_event: Event,  # 위에서 만든 새로운 이벤트 객체를 db에 추가하고 그 객체를 만환하는. mock_event 픽스처를 사용한다.
) -> None:  # mock_event 픽스처를 사용해 이벤트가 db에 추가되는지 테스트한다.
    response = await default_client.get("/event/")

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)

    # 웹 애플리케이션의 '/event/' 경로에 대해 GET 요청을 보내면, HTTP 상태 코드 200과 함께 생성된 mock event 정보가 올바르게 반환되어야 한다
