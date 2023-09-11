# 라우트를 등록하고 앱을 실행한다. 라이브러리와 사용자 라우트 정의를 임포트한다.
from fastapi import FastAPI
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

# uvicorn.run() 메서드를 사용해 8000번 포트에서 앱을 실행하도록 설정한다.
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
