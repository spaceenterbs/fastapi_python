from fastapi import FastAPI

app = FastAPI()  # app 변수에 FastAPI를 초기화해서 route를 생성한다. 여기서는 웰컴 라우트를 만든다.


@app.get("/")  # 데코레이터를 사용해 처리 유형을 정의하고 라우트가 호출될 때 실행할 처리를 함수를 지정한다.
async def welcome() -> dict:
    # GET 유형의 요청을 받아서 환영 메시지르르 반환하는 "/" 라우트를 만든다.
    return {
        "message": "Hello World",
    }
