# 데이터베이스 및 테이블 생성을 위한 설정을 작성한다.
from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

# 데이터베이스 파일의 위치(없는 경우 생성된다), 연결 문자열(connection string), 생성된 SQL 데이터베이스의 인스턴스를 변수에 저장한다.

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}
engine_url = create_engine(
    database_connection_string,
    echo=True,
    connect_args=connect_args,
)


def conn():  # SQLModel을 사용해서 db와 테이블을 생성한다.
    SQLModel.metadata.create_all(engine_url)


def get_session():  # db 세션을 앱 내에서 유지한다.
    with Session(engine_url) as session:
        yield session
