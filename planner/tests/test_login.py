import httpx
import pytest


# pytest.mark.asyncio 데코레이터를 추가해서 비동기 테스트라는 것을 명시한다.
# 다음과 같이 테스트 함수와 요청 페이로드를 정의해본다.
@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    """
    사용자 등록 라우트 테스트
    """
    payload = {
        "email": "testuser@packt.com",
        "password": "testpassword",
    }

    # 요청 헤더와 응답을 정의한다.
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    test_response = {
        "message": "User created successfully.",
    }

    # 요청에 대한 예상 응답을 정의한다.
    response = await default_client.post(
        "/user/signup",
        json=payload,
        headers=headers,
    )

    # 응답을 비교해서 요청이 성공했는지 확인하는 코드를 작성한다.
    assert response.status_code == 200
    assert response.json() == test_response


# 요청 페이로드와 헤더를 정의한다.
@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuser@packt.com",  # 사용자명을 다른 것으로 변경해서 테스트하면 실패한다.
        "password": "testpassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # 요청에 대한 예상 응답을 정의한다.
    response = await default_client.post(
        "/user/signin",
        data=payload,
        headers=headers,
    )

    # 응답을 비교해서 요청이 성공했는지 확인하는 코드를 작성한다.
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"
