# 라우트를 등록하고 앱을 실행한다. 라이브러리와 사용자 라우트 정의를 임포트한다.
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import List
from database.connection import conn

from routes.users import user_router
from routes.events import event_router

import uvicorn

app = FastAPI()
# 라우트 등록
app.include_router(
    user_router,
    prefix="/user",
)
app.include_router(
    event_router,
    prefix="/event",
)


# 앱이 시작될 때 db를 생성하도록 한다.
@app.on_event("startup")
def on_startup():
    conn()


# RedirectResponse는 상태 코드 307(리다이렉트)을 반환한다. 여기서는 "/"으로 접속한 경우 "/event/"로 리다이렉트하기 위해 사용한다.
@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


# uvicorn.run() 메서드를 사용해 8000번 포트에서 앱을 실행하도록 설정한다.
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
