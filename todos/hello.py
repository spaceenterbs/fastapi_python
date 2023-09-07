from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")  # 데코레이터를 사용해 처리 유형을 정의하고 라우트가 호출될 때 실행할 처리를 함수를 지정한다.
async def say_hello() -> dict:
    return {
        "message": "Hello!",
    }
