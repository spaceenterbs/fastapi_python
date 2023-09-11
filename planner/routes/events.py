# 이벤트 생성, 변경, 삭제 등의 처리를 위한 라우팅
from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

event_router = APIRouter(
    tags=["Event"],
)

events = []  # 이벤트 데이터를 관리하기 위한 목적. 데이터를 리스트에 추가하거나 삭제하는 데 사용된다.


# 모든 이벤트를 추출하거나 특정 ID의 이벤트만 추출하는 라우트를 정의한다.
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


# 특정 ID의 이벤트만 추출하는 라우트에서는 해당 ID의 이벤트가 없으면 HTTP_404_NOT_FOUND 예외를 발생시킨다.
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


# 이벤트 생성 및 삭제 라우트를 정의한다. 마지막은 전체 이벤트 삭제다.
@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    events.append(body)
    return {
        "message": "Event created successfully",
    }


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
