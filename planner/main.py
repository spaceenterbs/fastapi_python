# 라우트를 등록하고 앱을 실행한다. 라이브러리와 사용자 라우트 정의를 임포트한다.
from fastapi import FastAPI, Depends
from routes.users import user_router
from routes.events import event_router
from database.connection import Settings
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


from typing import Annotated
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()
settings = Settings()


# 출처 등록

# origins 배열을 등록하고
origins = ["*"]  # 어떤 출처(origin)에서 들어오는 요청을 허용할지 설정한다.

# add_middleware() 메서드를 사용해 미들웨어를 등록한다.
# 미들웨어는 각 요청과 응답 사이에서 작동하는 컴포넌트로, 여러 가지 기능(로그 생성, 오류 처리 등)을 수행할 수 있다.
app.add_middleware(
    CORSMiddleware,  # 추가하려는 미들웨어의 종류. 여기서는 CORS 관련 미들웨어를 사용한다.
    allow_origins=origins,  # 어떤 출처의 요청을 허용할지 결정한다. 위에서 정의한 origins 리스트를 사용한다.
    allow_credentials=True,  # 자격 증명(예: 쿠키나 HTTP Authentication 데이터)을 포함한 요청도 허용할지 결정한다.
    allow_methods=["*"],  # 어떤 HTTP 메서드(GET, POST 등)를 허용할지 결정한다.
    allow_headers=["*"],  # 어떤 HTTP 헤더를 허용할지 결정한다.
)

# 라우트 등록
app.include_router(
    user_router,
    prefix="/user",
)
app.include_router(
    event_router,
    prefix="/event",
)


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # 토큰 URL을 지정한다.


class User(BaseModel):
    """
    Pydantic usermodel
    """

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Security-First Steps
    """
    return {"token": token}


# 앱 실행 시 몽고DB를 초기화하도록 만든다.
@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


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
