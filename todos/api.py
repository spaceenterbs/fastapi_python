from fastapi import FastAPI
from todo import todo_router  # todo.py 파일에서 생성한 todo_router를 import한다.

app = FastAPI()  # app 변수에 FastAPI를 초기화해서 route를 생성한다. 여기서는 웰컴 라우트를 만든다.


@app.get("/")  # 데코레이터를 사용해 처리 유형을 정의하고 라우트가 호출될 때 실행할 처리를 함수를 지정한다.
async def welcome() -> dict:
    # GET 유형의 요청을 받아서 환영 메시지를 반환하는 "/" 라우트를 만든다.
    return {
        "message": "Hello World",
    }


app.include_router(todo_router)  # app 변수에 todo_router를 추가한다.

# 쉽게 테스트를 진행할 수 있도록 todos에 모든 파일을 모아서 작성한다.
