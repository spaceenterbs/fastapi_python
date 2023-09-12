# 이벤트 생성, 변경, 삭제 등의 처리를 위한 라우팅
from fastapi import APIRouter, Depends, Body, HTTPException, Request, status
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List
from sqlmodel import select

# Depends 클래스는 FastAPI 앱에서 의존성 주입(dependency injection)을 담당한다.
# 이 클래스는 함수를 인수로 사용하거나 함수 인수를 라우트에 전달할 수 있게 해서 어떤 처리가 실행되든지 필요한 의존성을 확보할 수 있게 해준다.

event_router = APIRouter(
    tags=["Event"],
)

events = []  # 이벤트 데이터를 관리하기 위한 목적. 데이터를 리스트에 추가하거나 삭제하는 데 사용된다.


# 모든 이벤트를 추출하거나 특정 ID의 이벤트만 추출하는 라우트를 정의한다.
@event_router.get(
    "/", response_model=List[Event]
)  # 전체 이벤트를 추출하는 GET 라우트를 변경해서 db에서 데이터를 가져오도록 만든다.
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(
        statement
    ).all()  # SQLAlchemy는 파이썬에서 db와 상호작용하기 위한 ORM(Object-Relational Mapping) 라이브러리다. exec() 메서드는 SQL 쿼리를 실행하고 결과를 반환한다.
    return events


# 특정 ID의 이벤트만 추출하는 라우트에서는 해당 ID의 이벤트가 없으면 HTTP_404_NOT_FOUND 예외를 발생시킨다.
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(
    id: int, session=Depends(get_session)
) -> Event:  # 지정한 ID의 이벤트 정보를 표시하는 라우트를 변경해서 db에서 데이터를 가져오도록 만든다.
    event = session.get(Event, id)
    if event:
        return event
    # for event in events:
    #     if event.id == id:
    #         return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


# 이벤트 생성 및 삭제 라우트를 정의한다. 마지막은 전체 이벤트 삭제다.
@event_router.post("/new")
# db 처리에 필요한 세션 객체가 get_session() 함수에 의존하도록 설정한다.
# 함수 내에서는 데이터(이벤트)를 세션에 추가하고 db에 등록(커밋)한 후 세션을 업데이트한다.
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        "message": "Event created successfully",
    }


# async def create_event(body: Event = Body(...)) -> dict:
#     events.append(body)
#     return {
#         "message": "Event created successfully",
#     }


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {
                "message": "Event deleted successfully",
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message": "All events deleted successfully",
    }


# 변경(update) 라우트는 실제 데이터베이스와 연동할 때 구현한다.
