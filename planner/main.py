# 라우트를 등록하고 앱을 실행한다. 라이브러리와 사용자 라우트 정의를 임포트한다.
from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
from database.connection import Settings

import uvicorn

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
settings = Settings()

# 라우트 등록
app.include_router(
    user_router,
    prefix="/user",
)
app.include_router(
    event_router,
    prefix="/event",
)

# 출처 등록

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 앱 실행 시 몽고DB를 초기화하도록 만든다.
@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


# uvicorn.run() 메서드를 사용해 9000(8000이 안돼~)번 포트에서 앱을 실행하도록 설정한다.
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=9000,
        reload=True,
    )
